#!/usr/bin/env python3
"""
Skeleton Code Generator: Python ODE Model
==========================================

This script generates a Python skeleton for an ODE-based Aedes population model
based on the UML class diagram specification.

The generated code provides:
- Class definitions matching UML structure
- Method signatures for all operations
- Placeholder implementations for vital rate functions
- Basic ODE integration setup using scipy

Usage:
    python generate_python_ode.py > aedes_ode_model.py

Author: Aedes UML Framework
License: MIT
"""

HEADER = '''#!/usr/bin/env python3
"""
Aedes Population ODE Model
==========================

Auto-generated skeleton from UML specification.
Fill in the equation implementations marked with TODO.

Based on: UML-Based Framework for Aedes Population Dynamics
Repository: https://github.com/sciom/aedes-uml-framework
"""

import numpy as np
from scipy.integrate import odeint
from dataclasses import dataclass
from typing import Optional, List, Tuple
from enum import Enum
from abc import ABC, abstractmethod

'''

ENUMS = '''
# ============================================================
# Enumerations
# ============================================================

class Sex(Enum):
    """Sex enumeration for adult mosquitoes."""
    MALE = "male"
    FEMALE = "female"


class SiteType(Enum):
    """Breeding site type enumeration."""
    CONTAINER = "container"
    TIRE = "tire"
    NATURAL = "natural"
    ARTIFICIAL = "artificial"

'''

LIFE_STAGES = '''
# ============================================================
# Life Stage Classes
# ============================================================

class LifeStage(ABC):
    """
    Abstract base class for all mosquito life stages.
    
    Attributes:
        abundance: Population count (state variable)
        development_rate: Stage-specific development rate
        mortality_rate: Stage-specific mortality rate
    """
    
    def __init__(self):
        self.abundance: float = 0.0
        self.development_rate: float = 0.0
        self.mortality_rate: float = 0.0
    
    @abstractmethod
    def develop(self, temp: float) -> float:
        """
        Calculate development rate as function of temperature.
        
        Args:
            temp: Daily mean temperature (°C)
            
        Returns:
            Development rate (1/day)
        """
        pass
    
    @abstractmethod
    def survive(self, rate: float) -> float:
        """
        Calculate survival probability.
        
        Args:
            rate: Mortality rate
            
        Returns:
            Survival probability (0-1)
        """
        pass
    
    def get_abundance(self) -> float:
        """Return current abundance."""
        return self.abundance


class AquaticStage(LifeStage):
    """
    Abstract class for aquatic life stages (egg, larva, pupa).
    Introduces density-dependent regulation.
    
    Attributes:
        carrying_capacity: Maximum population in habitat
        density_dependence_factor: Strength of density dependence
    """
    
    def __init__(self):
        super().__init__()
        self.carrying_capacity: float = 1000.0
        self.density_dependence_factor: float = 1.0
    
    def calculate_density_mortality(self, total_density: float) -> float:
        """
        Calculate density-dependent mortality modifier.
        
        Args:
            total_density: Total aquatic stage abundance in habitat
            
        Returns:
            Mortality modifier (≥1.0)
        """
        # TODO: Implement density-dependent mortality
        # Example: return 1.0 + (total_density / self.carrying_capacity)
        return 1.0 + self.density_dependence_factor * (total_density / self.carrying_capacity)


class Egg(AquaticStage):
    """
    Egg stage class.
    
    Attributes:
        hatching_threshold: Degree-days required for hatching
        diapause_state: Whether eggs are in diapause
        diapause_photoperiod_threshold: Critical photoperiod for diapause
        cold_tolerance: Minimum survival temperature
    """
    
    def __init__(self):
        super().__init__()
        self.hatching_threshold: float = 100.0  # degree-days
        self.diapause_state: bool = False
        self.diapause_photoperiod_threshold: float = 12.0  # hours
        self.cold_tolerance: float = -5.0  # °C
    
    def develop(self, temp: float) -> float:
        """Calculate egg development rate."""
        # TODO: Implement temperature-dependent development
        # Example Briere function: rate = a * temp * (temp - T_min) * sqrt(T_max - temp)
        if temp < 10.0 or temp > 35.0:
            return 0.0
        return 0.01 * temp  # Placeholder
    
    def survive(self, rate: float) -> float:
        """Calculate egg survival."""
        return np.exp(-rate)
    
    def hatch(self, temp: float, photoperiod: float) -> float:
        """
        Calculate hatching rate.
        
        Args:
            temp: Temperature (°C)
            photoperiod: Day length (hours)
            
        Returns:
            Hatching rate (proportion per day)
        """
        if self.diapause_state:
            return 0.0
        # TODO: Implement hatching function
        return self.develop(temp)
    
    def enter_diapause(self) -> None:
        """Induce diapause state."""
        self.diapause_state = True
    
    def exit_diapause(self, temp: float, photoperiod: float) -> None:
        """
        Check and potentially terminate diapause.
        
        Args:
            temp: Temperature (°C)
            photoperiod: Day length (hours)
        """
        if photoperiod > self.diapause_photoperiod_threshold and temp > 10.0:
            self.diapause_state = False
    
    def is_diapausing(self) -> bool:
        """Return diapause status."""
        return self.diapause_state


class Larva(AquaticStage):
    """
    Larval stage class with instar tracking.
    
    Attributes:
        instar_number: Current instar (1-4)
        instar_thresholds: Degree-days for each instar transition
        accumulated_degree_days: Cumulative thermal time
    """
    
    def __init__(self):
        super().__init__()
        self.instar_number: int = 1
        self.instar_thresholds: List[float] = [30.0, 60.0, 90.0, 120.0]
        self.accumulated_degree_days: float = 0.0
    
    def develop(self, temp: float) -> float:
        """Calculate larval development rate."""
        # TODO: Implement temperature-dependent development
        if temp < 10.0 or temp > 35.0:
            return 0.0
        return 0.015 * temp  # Placeholder
    
    def survive(self, rate: float) -> float:
        """Calculate larval survival with density dependence."""
        return np.exp(-rate)
    
    def moult(self) -> None:
        """Advance to next instar."""
        if self.instar_number < 4:
            self.instar_number += 1
            self.accumulated_degree_days = 0.0
    
    def pupate(self) -> float:
        """
        Calculate pupation rate for L4 larvae.
        
        Returns:
            Pupation rate (proportion per day)
        """
        if self.instar_number == 4:
            # TODO: Implement pupation threshold check
            return 0.1  # Placeholder
        return 0.0
    
    def feeding_rate(self, temp: float) -> float:
        """
        Calculate feeding rate.
        
        Args:
            temp: Temperature (°C)
            
        Returns:
            Relative feeding rate
        """
        # TODO: Implement temperature-dependent feeding
        return max(0, (temp - 10) / 20)


class Pupa(AquaticStage):
    """
    Pupal stage class.
    
    Attributes:
        emergence_threshold: Degree-days required for emergence
        accumulated_degree_days: Cumulative thermal time
    """
    
    def __init__(self):
        super().__init__()
        self.emergence_threshold: float = 50.0
        self.accumulated_degree_days: float = 0.0
    
    def develop(self, temp: float) -> float:
        """Calculate pupal development rate."""
        # TODO: Implement temperature-dependent development
        if temp < 10.0 or temp > 35.0:
            return 0.0
        return 0.02 * temp  # Placeholder
    
    def survive(self, rate: float) -> float:
        """Calculate pupal survival."""
        return np.exp(-rate)
    
    def emerge(self) -> float:
        """
        Calculate emergence rate.
        
        Returns:
            Emergence rate (proportion per day)
        """
        # TODO: Implement emergence threshold check
        return 0.15  # Placeholder
    
    def calculate_emergence_time(self, temp: float) -> float:
        """
        Estimate time to emergence.
        
        Args:
            temp: Temperature (°C)
            
        Returns:
            Days until emergence
        """
        rate = self.develop(temp)
        if rate > 0:
            return self.emergence_threshold / rate
        return float('inf')


class Adult(LifeStage):
    """
    Adult stage class.
    
    Attributes:
        sex: MALE or FEMALE
        gonotrophic_cycle_day: Current day in cycle
        gonotrophic_cycle_length: Total cycle length
        bloodfed_status: Whether recently bloodfed
        mated_status: Whether mated
        fecundity: Eggs per oviposition
        flight_range: Maximum dispersal distance
    """
    
    def __init__(self, sex: Sex = Sex.FEMALE):
        super().__init__()
        self.sex: Sex = sex
        self.gonotrophic_cycle_day: int = 0
        self.gonotrophic_cycle_length: int = 4
        self.bloodfed_status: bool = False
        self.mated_status: bool = False
        self.fecundity: float = 100.0
        self.flight_range: float = 200.0  # meters
    
    def develop(self, temp: float) -> float:
        """Calculate adult development (gonotrophic cycle)."""
        # TODO: Implement temperature-dependent gonotrophic cycle
        if temp < 15.0 or temp > 35.0:
            return 0.0
        return 0.25 * (temp - 15) / 10  # Placeholder
    
    def survive(self, rate: float) -> float:
        """Calculate adult survival."""
        return np.exp(-rate)
    
    def mate(self) -> None:
        """Set mated status."""
        self.mated_status = True
    
    def seek_host(self) -> float:
        """
        Calculate host-seeking success rate.
        
        Returns:
            Probability of successful blood meal
        """
        # TODO: Implement host-seeking model
        return 0.3  # Placeholder
    
    def blood_feed(self) -> None:
        """Record blood meal and start gonotrophic cycle."""
        self.bloodfed_status = True
        self.gonotrophic_cycle_day = 0
    
    def develop_eggs(self, temp: float) -> None:
        """
        Advance gonotrophic cycle.
        
        Args:
            temp: Temperature (°C)
        """
        rate = self.develop(temp)
        self.gonotrophic_cycle_day += rate
    
    def oviposit(self) -> int:
        """
        Calculate eggs laid.
        
        Returns:
            Number of eggs deposited
        """
        if self.is_gravid():
            self.bloodfed_status = False
            self.gonotrophic_cycle_day = 0
            return int(self.fecundity)
        return 0
    
    def is_gravid(self) -> bool:
        """Check if ready to oviposit."""
        return (self.bloodfed_status and 
                self.gonotrophic_cycle_day >= self.gonotrophic_cycle_length)

'''

ENVIRONMENT = '''
# ============================================================
# Environmental Driver Classes
# ============================================================

@dataclass
class Coordinates:
    """Geographic coordinates."""
    latitude: float
    longitude: float


class Temperature:
    """
    Temperature driver class.
    
    Attributes:
        daily_mean: Mean daily temperature (°C)
        daily_min: Minimum daily temperature (°C)
        daily_max: Maximum daily temperature (°C)
    """
    
    def __init__(self):
        self.daily_mean: float = 20.0
        self.daily_min: float = 15.0
        self.daily_max: float = 25.0
        self.historical_data: List[float] = []
    
    def update(self, date: int) -> None:
        """
        Update temperature for given date.
        
        Args:
            date: Day of year (1-365)
        """
        # TODO: Implement temperature forcing
        # Example: seasonal sinusoid
        self.daily_mean = 20 + 10 * np.sin(2 * np.pi * (date - 91) / 365)
        self.daily_min = self.daily_mean - 5
        self.daily_max = self.daily_mean + 5
    
    def get_development_modifier(self, base_rate: float) -> float:
        """
        Calculate temperature-modified development rate.
        
        Args:
            base_rate: Base development rate
            
        Returns:
            Modified development rate
        """
        # TODO: Implement temperature response function
        return base_rate * max(0, (self.daily_mean - 10) / 15)
    
    def get_mortality_modifier(self, base_rate: float) -> float:
        """
        Calculate temperature-modified mortality rate.
        
        Args:
            base_rate: Base mortality rate
            
        Returns:
            Modified mortality rate
        """
        # TODO: Implement temperature-mortality relationship
        if self.daily_mean < 5 or self.daily_mean > 40:
            return base_rate * 5  # High mortality at extremes
        return base_rate
    
    def calculate_degree_days(self, threshold: float) -> float:
        """
        Calculate degree-days above threshold.
        
        Args:
            threshold: Base temperature (°C)
            
        Returns:
            Degree-days accumulated
        """
        return max(0, self.daily_mean - threshold)


class Precipitation:
    """
    Precipitation driver class.
    
    Attributes:
        daily_amount: Daily precipitation (mm)
        cumulative_weekly: 7-day cumulative (mm)
        cumulative_monthly: 30-day cumulative (mm)
    """
    
    def __init__(self):
        self.daily_amount: float = 0.0
        self.cumulative_weekly: float = 0.0
        self.cumulative_monthly: float = 0.0
    
    def update(self, date: int) -> None:
        """
        Update precipitation for given date.
        
        Args:
            date: Day of year (1-365)
        """
        # TODO: Implement precipitation forcing
        # Example: stochastic with seasonal pattern
        self.daily_amount = max(0, np.random.normal(2, 3))
    
    def get_habitat_availability(self) -> float:
        """
        Calculate relative habitat availability.
        
        Returns:
            Habitat availability index (0-1)
        """
        # TODO: Implement rainfall-habitat relationship
        return min(1.0, self.cumulative_weekly / 50)
    
    def get_flooding_risk(self) -> float:
        """
        Calculate flooding mortality risk.
        
        Returns:
            Flooding risk index (0-1)
        """
        if self.daily_amount > 50:
            return 0.5
        return 0.0


class Environment:
    """
    Environment container class.
    
    Attributes:
        current_date: Day of year
        latitude: Geographic latitude
        temperature: Temperature driver
        precipitation: Precipitation driver
    """
    
    def __init__(self, latitude: float = 45.0):
        self.current_date: int = 1
        self.latitude: float = latitude
        self.temperature: Temperature = Temperature()
        self.precipitation: Precipitation = Precipitation()
    
    def advance_day(self) -> None:
        """Advance simulation by one day."""
        self.current_date = (self.current_date % 365) + 1
        self.temperature.update(self.current_date)
        self.precipitation.update(self.current_date)
    
    def get_photoperiod(self) -> float:
        """
        Calculate day length based on latitude and date.
        
        Returns:
            Photoperiod in hours
        """
        # Approximate photoperiod calculation
        lat_rad = np.radians(self.latitude)
        declination = 23.45 * np.sin(2 * np.pi * (284 + self.current_date) / 365)
        decl_rad = np.radians(declination)
        
        cos_hour_angle = -np.tan(lat_rad) * np.tan(decl_rad)
        cos_hour_angle = np.clip(cos_hour_angle, -1, 1)
        hour_angle = np.arccos(cos_hour_angle)
        
        return 2 * np.degrees(hour_angle) / 15

'''

CONTROL = '''
# ============================================================
# Control Measure Classes
# ============================================================

class ControlMeasure(ABC):
    """
    Abstract base class for control interventions.
    
    Attributes:
        efficacy: Maximum efficacy (0-1)
        application_date: Day of application
        duration: Duration of effect (days)
        cost: Cost per application
    """
    
    def __init__(self):
        self.efficacy: float = 0.9
        self.application_date: int = 0
        self.duration: int = 14
        self.cost: float = 100.0
    
    @abstractmethod
    def apply(self) -> None:
        """Apply the control measure."""
        pass
    
    def is_active(self, current_date: int) -> bool:
        """Check if control is still active."""
        days_since = current_date - self.application_date
        return 0 <= days_since <= self.duration
    
    def get_residual_efficacy(self, days_since_application: int) -> float:
        """
        Calculate residual efficacy.
        
        Args:
            days_since_application: Days since control was applied
            
        Returns:
            Current efficacy (0-1)
        """
        if days_since_application > self.duration:
            return 0.0
        # Exponential decay
        decay_rate = 0.1
        return self.efficacy * np.exp(-decay_rate * days_since_application)


class Larvicide(ControlMeasure):
    """
    Larvicide control measure.
    
    Attributes:
        target_instars: Which instars are affected
        resistance_factor: Resistance level (0-1)
    """
    
    def __init__(self):
        super().__init__()
        self.target_instars: List[int] = [1, 2, 3, 4]
        self.resistance_factor: float = 0.0
    
    def apply(self) -> None:
        """Apply larvicide."""
        # TODO: Implement site-specific application
        pass
    
    def calculate_mortality_increase(self, instar: int) -> float:
        """
        Calculate additional mortality from larvicide.
        
        Args:
            instar: Larval instar (1-4)
            
        Returns:
            Additional mortality rate
        """
        if instar in self.target_instars:
            return self.efficacy * (1 - self.resistance_factor)
        return 0.0


class Adulticide(ControlMeasure):
    """
    Adulticide control measure.
    
    Attributes:
        spray_radius: Effective radius (meters)
        wind_sensitivity: Effect of wind on efficacy
    """
    
    def __init__(self):
        super().__init__()
        self.spray_radius: float = 100.0
        self.wind_sensitivity: float = 0.5
    
    def apply(self) -> None:
        """Apply adulticide."""
        # TODO: Implement spatial application
        pass
    
    def calculate_mortality_increase(self) -> float:
        """
        Calculate additional adult mortality.
        
        Returns:
            Additional mortality rate
        """
        return self.efficacy

'''

ODE_MODEL = '''
# ============================================================
# ODE Model Implementation
# ============================================================

class AedesODEModel:
    """
    ODE-based Aedes population model.
    
    State vector: [E, L1, L2, L3, L4, P, A_m, A_f]
    where:
        E = Eggs
        L1-L4 = Larval instars
        P = Pupae
        A_m = Adult males
        A_f = Adult females
    """
    
    def __init__(self):
        self.env = Environment()
        self.egg = Egg()
        self.larva = Larva()
        self.pupa = Pupa()
        self.adult = Adult()
        
        # Model parameters
        self.params = {
            'mu_E': 0.01,    # Egg mortality
            'mu_L': 0.05,    # Larval mortality (base)
            'mu_P': 0.02,    # Pupal mortality
            'mu_A': 0.1,     # Adult mortality
            'K': 1000,       # Carrying capacity
            'f': 100,        # Fecundity
            'sex_ratio': 0.5 # Proportion female
        }
    
    def derivatives(self, y: np.ndarray, t: float) -> np.ndarray:
        """
        Calculate derivatives for ODE system.
        
        Args:
            y: State vector [E, L1, L2, L3, L4, P, A_m, A_f]
            t: Time
            
        Returns:
            Derivatives dy/dt
        """
        E, L1, L2, L3, L4, P, A_m, A_f = y
        
        # Get environmental conditions
        self.env.current_date = int(t) % 365 + 1
        self.env.temperature.update(self.env.current_date)
        temp = self.env.temperature.daily_mean
        
        # Calculate rates
        # TODO: Replace with actual temperature-dependent functions
        d_E = self.egg.develop(temp)
        d_L = self.larva.develop(temp)
        d_P = self.pupa.develop(temp)
        
        mu_E = self.params['mu_E']
        mu_L = self.params['mu_L']
        mu_P = self.params['mu_P']
        mu_A = self.params['mu_A']
        
        # Density dependence
        total_L = L1 + L2 + L3 + L4
        dd_factor = 1 + total_L / self.params['K']
        mu_L_dd = mu_L * dd_factor
        
        # Fecundity
        f = self.params['f']
        r = self.params['sex_ratio']
        
        # Derivatives
        dE = f * A_f - (d_E + mu_E) * E
        dL1 = d_E * E - (d_L + mu_L_dd) * L1
        dL2 = d_L * L1 - (d_L + mu_L_dd) * L2
        dL3 = d_L * L2 - (d_L + mu_L_dd) * L3
        dL4 = d_L * L3 - (d_L + mu_L_dd) * L4
        dP = d_L * L4 - (d_P + mu_P) * P
        dA_m = (1 - r) * d_P * P - mu_A * A_m
        dA_f = r * d_P * P - mu_A * A_f
        
        return np.array([dE, dL1, dL2, dL3, dL4, dP, dA_m, dA_f])
    
    def simulate(self, y0: np.ndarray, t_span: Tuple[float, float], 
                 dt: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Run simulation.
        
        Args:
            y0: Initial state vector
            t_span: (start_time, end_time)
            dt: Time step
            
        Returns:
            Tuple of (times, states)
        """
        t = np.arange(t_span[0], t_span[1], dt)
        y = odeint(self.derivatives, y0, t)
        return t, y


# ============================================================
# Main Execution
# ============================================================

if __name__ == "__main__":
    # Example usage
    model = AedesODEModel()
    
    # Initial conditions
    y0 = np.array([1000, 0, 0, 0, 0, 0, 0, 10])  # 1000 eggs, 10 females
    
    # Simulate one year
    t, y = model.simulate(y0, (0, 365))
    
    # Print results
    print("Simulation complete!")
    print(f"Final state:")
    print(f"  Eggs: {y[-1, 0]:.0f}")
    print(f"  Larvae (total): {y[-1, 1:5].sum():.0f}")
    print(f"  Pupae: {y[-1, 5]:.0f}")
    print(f"  Adults: {y[-1, 6:].sum():.0f}")
'''

def generate():
    """Generate complete Python skeleton."""
    print(HEADER)
    print(ENUMS)
    print(LIFE_STAGES)
    print(ENVIRONMENT)
    print(CONTROL)
    print(ODE_MODEL)

if __name__ == "__main__":
    generate()
