import argparse
import io
import random

import imageio
import matplotlib.pyplot as plt
import numpy as np

DIRECTION_MAPPING = {
    'up': '^',
    'down': 'v',
    'left': '<',
    'right': '>'
}


def initialize_grids(grid_size_x: int, grid_size_y: int) -> tuple:
    """
    Initialize nutrient and repellent grids with radial gradients.

    Parameters
    ----------
    grid_size_x : int
        The horizontal size of the grid.
    grid_size_y : int
        The vertical size of the grid.

    Returns
    -------
    tuple
        Tuple containing the nutrient grid and repellent grid.
        Each grid is a 2D numpy array.
    """
    nutrient_grid = np.zeros((grid_size_x, grid_size_y))
    repellent_grid = np.zeros((grid_size_x, grid_size_y))
    center_x, center_y = grid_size_x // 2, grid_size_y // 2

    # Populate grids with radial gradients
    for x in range(grid_size_x):
        for y in range(grid_size_y):
            distance_to_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            nutrient_grid[x, y] = np.exp(-distance_to_center / 20.0)
            repellent_grid[x, y] = 1 - np.exp(-distance_to_center / 20.0)

    return nutrient_grid, repellent_grid


def initialize_nematode(grid_size_x: int, grid_size_y: int) -> list:
    """
    Initialize the starting position of nematode.

    Parameters
    ----------
    grid_size_x : int
        The horizontal size of the grid.
    grid_size_y : int
        The vertical size of the grid.
    option : str, optional
        The initialization option. The default is 'center'.

    Returns
    -------
    list
        List containing the starting position of nematode.
    """

    x = random.randint(0, grid_size_x - 1)
    y = random.randint(0, grid_size_y - 1)
    return [(x, y)]


def get_level(x: int, y: int, grid: np.ndarray) -> float:
    """
    Get the nutrient or repellent level at a specific position in a grid.

    Parameters
    ----------
    x : int
        The horizontal position in the grid.
    y : int
        The vertical position in the grid.
    grid : np.ndarray
        The grid to get the level from.

    Returns
    -------
    float
        The nutrient or repellent level at the given position.
    """
    if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
        return grid[x, y]
    else:
        return 0


def visualize_state(grid: np.ndarray, nematode, time_step: int) -> None:
    """
    Visualize the current state of the simulation.

    Parameters
    ----------
    grid : np.ndarray
        The grid to visualize.
    nematode_positions : list
        List containing the nematode positions.
    time_step : int
        The current time step.
    """
    
    nematode_x, nematode_y = nematode.position
    orientation = DIRECTION_MAPPING[nematode.orientation]
    
    plt.imshow(grid, cmap='viridis')
    plt.scatter(nematode_y, nematode_x, c='red', label='Nematode', marker=orientation)
    plt.colorbar(label='Nutrient Concentration')
    plt.title(f'Time step {time_step}')

    # Remove tick labels
    plt.xticks([])
    plt.yticks([])

    plt.pause(0.1)

    # Save image to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Read image from buffer
    image_array = imageio.v2.imread(buf)

    # Clear buffer and plot
    plt.clf()

    return image_array


class Nematode:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.previous_concentration = 0
        self.orientation = 'up'

    def move(self, simulation):

        nearby_positions = self.nearby

        bias = np.ones(len(nearby_positions)) / len(nearby_positions)

        bias /= np.sum(bias)
        new_x, new_y = nearby_positions[np.random.choice(range(4), p=bias)]

        # Apply boundary conditions
        new_x = min(max(0, new_x), simulation.grid_size_x - 1)
        new_y = min(max(0, new_y), simulation.grid_size_y - 1)

        self.position = (new_x, new_y)

        self.previous_concentration = get_level(
            new_x, new_y, simulation.nutrient_grid)

        return new_x, new_y
    
    @property
    def in_front(self):
        if self.orientation == 'up':
            return (self.x, self.y-1)
        elif self.orientation == 'down':
            return (self.x, self.y+1)
        elif self.orientation == 'left':
            return (self.x-1, self.y)
        elif self.orientation == 'right':
            return (self.x+1, self.y)
        
    @property
    def collision(self):
        return self.in_front in [nematode.position for nematode in simulation.nematode]
        
    @property
    def nearby(self):
        return [(self.x-1, self.y), (self.x+1, self.y),
                (self.x, self.y-1), (self.x, self.y+1)]

    @property
    def position(self):
        return (self.x, self.y)

    @position.setter
    def position(self, new_position):
        self.x, self.y = new_position


class Simulation:

    def __init__(self, time_steps: int,
                 grid_size_x: int,
                 grid_size_y: int):

        self.time_steps = time_steps
        self.grid_size_x = grid_size_x
        self.grid_size_y = grid_size_y

        self.nematode_positions = initialize_nematode(
            self.grid_size_x, self.grid_size_y)

        self.nutrient_grid, self.repellent_grid = initialize_grids(
            self.grid_size_x, self.grid_size_y)

        self._setup()

    def _setup(self):
        self.nematode = [Nematode(x, y) for x, y in self.nematode_positions]

    def _simulate(self, t: int):
        new_positions = []
        for nematode in self.nematode:
            # Get next move
            new_x, new_y = nematode.move(self)

            new_positions.append((new_x, new_y))

        # Update nematode positions for the next iteration
        self.nematode_positions = new_positions

        # Visualize the simulation state every 10 time steps
        if t % 1 == 0:
            image = visualize_state(
                self.nutrient_grid, nematode, t)

            self.image_list.append(image)

    def simulate(self) -> None:
        """ 
        Simulate the movement of nematode in a grid.

        Parameters
        ----------
        grid_size_x : int
            The horizontal size of the grid.
        grid_size_y : int
            The vertical size of the grid.
        move_function : str
            The move function to use
        """

        self.image_list = []

        # Main simulation loop
        for t in range(self.time_steps):
            self._simulate(t)

        # Save the results in a GIF
        imageio.mimsave('nematode.gif', self.image_list, fps=20)

    def get_levels(self, nematode: Nematode, level_name: str):
        return [get_level(x, y, getattr(self, f'{level_name}_grid')) for x, y in nematode.nearby]


if __name__ == '__main__':

    # command line update defaults
    parser = argparse.ArgumentParser(description='Nematode simulation')
    parser.add_argument('--time_steps', type=int,
                        default=100, help='number of time steps')
    parser.add_argument('--grid_size_x', type=int,
                        default=25, help='grid size x')
    parser.add_argument('--grid_size_y', type=int,
                        default=25, help='grid size y')

    args = parser.parse_args()

    simulation = Simulation(
        args.time_steps, args.grid_size_x, args.grid_size_y)

    simulation.simulate()
