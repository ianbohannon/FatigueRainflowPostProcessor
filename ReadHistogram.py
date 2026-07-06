import numpy as np


def calculate_N(data):
    """
    Calculates the 'N' value for each row based on stress.

    Formula:
    - If stress < 92.682982338837: N = 10^15.835 / (stress^5)
    - Otherwise: N = 10^11.901 / (stress^3)

    Parameters:
    -----------
    data : numpy.ndarray
        A 2D numpy array with shape (n, 2) where:
        - Column 0: Stress values
        - Column 1: Cycle values

    Returns:
    --------
    numpy.ndarray
        A 1D array containing the calculated 'N' values for each row

    Example:
    --------
    >>> data = read_fatigue_data('Input/FatigueRainflowTest.$26')
    >>> N_values = calculate_N(data)
    """
    stress = data[:, 0]

    # Initialize N array
    N = np.zeros(len(data))

    # Apply the conditional formula based on stress threshold
    # If stress < 92.682982338837: N = 10^15.835 / (stress^5)
    low_stress_mask = stress < 92.682982338837
    N[low_stress_mask] = (10**15.835) / (stress[low_stress_mask]**5)

    # Otherwise: N = 10^11.901 / (stress^3)
    high_stress_mask = ~low_stress_mask
    N[high_stress_mask] = (10**11.901) / (stress[high_stress_mask]**3)

    return N


def calculate_fatigue(data, N_values):
    """
    Calculates the fatigue for each row using the formula: fatigue = n/N

    Parameters:
    -----------
    data : numpy.ndarray
        A 2D numpy array with shape (n, 2) where:
        - Column 0: Stress values
        - Column 1: Cycle values (n)
    N_values : numpy.ndarray
        A 1D array containing the calculated 'N' values for each row

    Returns:
    --------
    numpy.ndarray
        A 1D array containing the calculated fatigue values for each row

    Example:
    --------
    >>> data = read_fatigue_data('Input/FatigueRainflowTest.$26')
    >>> N_values = calculate_N(data)
    >>> fatigue = calculate_fatigue(data, N_values)
    """
    n = data[:, 1]  # cycles from the input matrix

    # Calculate fatigue = n/N
    # Handle division by zero (return 0 for fatigue when N is 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        fatigue = np.divide(n, N_values)
        fatigue = np.nan_to_num(fatigue, nan=0.0, posinf=0.0, neginf=0.0)

    return fatigue


def calculate_total_fatigue(fatigue):
    """
    Calculates the total fatigue by summing all individual fatigue values.

    Parameters:
    -----------
    fatigue : numpy.ndarray
        A 1D array containing the calculated fatigue values for each row

    Returns:
    --------
    float
        The total fatigue (sum of all rows)

    Example:
    --------
    >>> data = read_fatigue_data('Input/FatigueRainflowTest.$26')
    >>> N_values = calculate_N(data)
    >>> fatigue = calculate_fatigue(data, N_values)
    >>> total_fatigue = calculate_total_fatigue(fatigue)
    """
    return fatigue.sum()


def calculate_lifespan(design_life, total_fatigue):
    """
    Calculates the lifespan based on design life and total fatigue.

    Formula: lifespan = design_life / total_fatigue

    Parameters:
    -----------
    design_life : float
        The design life in years
    total_fatigue : float
        The total fatigue (sum of all fatigue values)

    Returns:
    --------
    float
        The calculated lifespan in years

    Example:
    --------
    >>> design_life = 20
    >>> lifespan = calculate_lifespan(design_life, total_fatigue)
    """
    return design_life / total_fatigue


def read_fatigue_data(filepath):
    """
    Reads a fatigue data file containing stress and cycle data.

    Parameters:
    -----------
    filepath : str
        Path to the fatigue data file

    Returns:
    --------
    numpy.ndarray
        A 2D numpy array with shape (n, 2) where:
        - Column 0: Stress values
        - Column 1: Cycle values

    Example:
    --------
    >>> data = read_fatigue_data('Input/FatigueRainflowTest.$26')
    >>> print(data.shape)  # (128, 2)
    >>> stress = data[:, 0]
    >>> cycles = data[:, 1]
    """
    try:
        # Read the file using numpy's loadtxt function
        # It automatically handles scientific notation
        data = np.loadtxt(filepath)

        return data

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except ValueError as e:
        raise ValueError(f"Error parsing file {filepath}: {e}")
    except Exception as e:
        raise Exception(f"Error reading file {filepath}: {e}")
