# Rocket Flight Simulation

A Python-based rocket flight simulation that models the vertical motion of a rocket from launch until it returns to the ground.

The simulation allows the user to change rocket, engine, atmospheric, and gravitational parameters and observe how they affect the rocket's altitude, velocity, and flight duration.

## Features

The simulation includes:

- Variable rocket mass as fuel is consumed
- User-defined engine thrust
- User-defined fuel mass and burn rate
- Aerodynamic drag
- Atmospheric density decreasing with altitude
- Configurable gravity for different celestial bodies
- Automatic engine cutoff when fuel is depleted
- Automatic detection of the rocket returning to the ground
- Maximum altitude calculation
- Maximum velocity calculation
- Total flight time calculation
- Altitude and velocity graphs

## Physics Model

The rocket is modeled using numerical integration of differential equations.

### Rocket Mass

The total mass changes during flight as fuel is consumed:

`Total Mass = Empty Rocket Mass + Remaining Fuel Mass`

### Thrust

The engine produces constant thrust while fuel remains.

When the fuel reaches zero, thrust becomes zero and the rocket continues its flight under gravity and aerodynamic drag.

### Atmospheric Density

Air density decreases exponentially with altitude:

`ρ = ρ₀ × exp(-h / H)`

where:

- `ρ₀ = 1.225 kg/m³` is sea-level air density
- `h` is altitude
- `H = 8500 m` is the atmospheric scale height

### Aerodynamic Drag

Drag is calculated using:

`F_drag = 0.5 × ρ × v² × Cd × A`

where:

- `ρ` = air density
- `v` = rocket velocity
- `Cd` = drag coefficient
- `A` = rocket cross-sectional area

### Rocket Acceleration

The rocket's acceleration is calculated from thrust, drag, gravity, and the rocket's changing mass.

The differential equations are solved numerically using SciPy's `solve_ivp`.

## User Inputs

When the program starts, the user can enter:

- Gravitational acceleration
- Empty rocket mass
- Initial fuel mass
- Engine thrust
- Fuel consumption rate
- Drag coefficient
- Rocket cross-sectional area

Pressing **Enter** without entering a value uses the default value.

Example gravity values included in the program:

| Location | Gravity |
|---|---:|
| Earth | 9.81 m/s² |
| Mars | 3.71 m/s² |
| Moon | 1.62 m/s² |

## Default Rocket Parameters

| Parameter | Default Value |
|---|---:|
| Empty mass | 50 kg |
| Fuel mass | 150 kg |
| Engine thrust | 5000 N |
| Fuel burn rate | 5 kg/s |
| Drag coefficient | 0.5 |
| Cross-sectional area | 0.05 m² |
| Gravity | 9.81 m/s² |

With the default values, the calculated engine burn time is:

`150 kg / 5 kg/s = 30 seconds`

## Output

After the simulation finishes, the program reports:

- Maximum altitude (apogee)
- Maximum velocity
- Approximate Mach number
- Engine cutoff time
- Total flight duration

It also generates two graphs:

1. **Altitude vs. Time**
2. **Velocity vs. Time**

The engine cutoff time is marked on the graphs.

The resulting figure is saved automatically as:

`rocket_trajectory.png`

## Project Files

- `rocket_simulation.py` — Main simulation code
- `requirements.txt` — Required Python libraries
- `README.md` — Project documentation

## Requirements

The project uses:

- Python
- NumPy
- SciPy
- Matplotlib

Install the required packages using: pip install -r requirements.txt

Run the simulation using: python3 rocket_simulation.py
