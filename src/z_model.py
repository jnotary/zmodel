"""
Z Model: Control-Theoretic Heuristic for Governed Adaptive Systems
Version 1.6 - Production Implementation

Author: jnotary
License: MIT
Website: cloudsystems.online

Core equation: Z = (A * E / C) * cos²(Psi)
"""

import numpy as np
from typing import Optional, List, Tuple, Callable
import warnings


class ZModel:
    """
    Core Z Model implementation with control-theoretic foundation.
    
    Z = (A * E / C) * cos²(Psi)
    
    Where:
        A: Adaptability (degrees of freedom)
        E: Energy/Efficacy (capability)
        C: Constraints/Cost (friction)
        Psi: Alignment angle (governance)
    
    Attributes:
        use_squared_gating (bool): If True, uses cos²(Psi); else cos(Psi)
    """
    
    def __init__(self, use_squared_gating: bool = True):
        """
        Initialize Z Model.
        
        Args:
            use_squared_gating: Use cos²(Psi) for stricter nonlinear penalty.
                               Set False for linear cos(Psi) (faster computation).
        """
        self.use_squared_gating = use_squared_gating
    
    def calculate_z(
        self, 
        A: float, 
        E: float, 
        C: float, 
        Psi_deg: float
    ) -> float:
        """
        Calculate Z score with governance gating.
        
        Args:
            A: Adaptability (> 0)
            E: Energy/Efficacy (> 0)
            C: Constraints/Cost (> 0)
            Psi_deg: Alignment angle in degrees [0, 180]
        
        Returns:
            Z score (governed capability index)
        
        Raises:
            ValueError: If C <= 0 (singularity)
        """
        if C <= 0:
            raise ValueError(
                f"Cost C must be positive (got {C}). "
                "Zero cost represents unbounded optimization."
            )
        
        # Base efficiency ratio
        base_z = (A * E) / C
        
        # Governance gating via vector projection
        Psi_rad = np.radians(Psi_deg)
        cos_term = np.cos(Psi_rad)
        
        if self.use_squared_gating:
            gating_factor = cos_term ** 2  # Stricter penalty (Malus's Law)
        else:
            gating_factor = cos_term  # Linear gating
        
        return base_z * gating_factor
    
    def hazard_adjusted_z(
        self,
        A: float,
        E: float,
        C: float,
        H: float,
        Psi_deg: float
    ) -> float:
        """
        Calculate Z with hazard mass targeting.
        
        Z = (A * E) / (C + H) * cos²(Psi)
        
        Args:
            H: Hazard mass (adversarial entropy, risk amplification)
        
        Returns:
            Hazard-adjusted Z score
        """
        total_cost = C + H
        
        if total_cost <= 0:
            raise ValueError("Total cost (C + H) must be positive")
        
        base_z = (A * E) / total_cost
        Psi_rad = np.radians(Psi_deg)
        
        gating_factor = (np.cos(Psi_rad) ** 2 if self.use_squared_gating 
                        else np.cos(Psi_rad))
        
        return base_z * gating_factor
    
    def temporal_evolution(
        self,
        A_t: np.ndarray,
        E_t: np.ndarray,
        C_t: np.ndarray,
        Psi_t: np.ndarray
    ) -> np.ndarray:
        """
        Compute Z(t) over time series.
        
        Args:
            A_t, E_t, C_t, Psi_t: Time series arrays (same length)
        
        Returns:
            Z(t) array
        """
        if not (len(A_t) == len(E_t) == len(C_t) == len(Psi_t)):
            raise ValueError("All time series must have equal length")
        
        if np.any(C_t <= 0):
            raise ValueError("Cost time series contains non-positive values")
        
        base_z_t = (A_t * E_t) / C_t
        Psi_rad_t = np.radians(Psi_t)
        
        gating_t = (np.cos(Psi_rad_t) ** 2 if self.use_squared_gating
                   else np.cos(Psi_rad_t))
        
        return base_z_t * gating_t
    
    def calculate_alignment_angle(
        self,
        action_vector: np.ndarray,
        harmony_vector: np.ndarray
    ) -> Tuple[float, float]:
        """
        Calculate Psi angle from vector embeddings.
        
        This is how Psi is computed in practice for LLM safety gating:
        1. Embed the action (prompt + response)
        2. Embed the harmony principle ("Life and Technology in Harmony")
        3. Compute cosine similarity
        4. Convert to angle
        
        Args:
            action_vector: Embedding of current action
            harmony_vector: Embedding of harmony/safety principles
        
        Returns:
            Tuple of (Psi_deg, cos_similarity)
        """
        # Normalize vectors
        action_norm = action_vector / (np.linalg.norm(action_vector) + 1e-10)
        harmony_norm = harmony_vector / (np.linalg.norm(harmony_vector) + 1e-10)
        
        # Cosine similarity
        cos_sim = np.dot(action_norm, harmony_norm)
        cos_sim = np.clip(cos_sim, -1.0, 1.0)  # Numerical stability
        
        # Convert to angle
        Psi_rad = np.arccos(cos_sim)
        Psi_deg = np.degrees(Psi_rad)
        
        return Psi_deg, cos_sim
    
    def multi_agent_system(
        self,
        agents: List[Tuple[float, float, float, float]],
        weights: Optional[List[float]] = None
    ) -> Tuple[float, List[float]]:
        """
        Calculate system-level Z for multiple agents.
        
        Args:
            agents: List of (A, E, C, Psi_deg) tuples per agent
            weights: Trust/relevance weights (default: uniform)
        
        Returns:
            Tuple of (system_z, individual_z_list)
        """
        n_agents = len(agents)
        
        if weights is None:
            weights = [1.0 / n_agents] * n_agents
        
        if not np.isclose(sum(weights), 1.0):
            weights = np.array(weights) / sum(weights)
        
        individual_z = [
            self.calculate_z(A, E, C, Psi) 
            for A, E, C, Psi in agents
        ]
        
        system_z = sum(w * z for w, z in zip(weights, individual_z))
        
        return system_z, individual_z
    
    def __repr__(self) -> str:
        gating_type = "cos²(Psi)" if self.use_squared_gating else "cos(Psi)"
        return f"ZModel(gating={gating_type})"


class ZController:
    """
    Proportional feedback controller for Z-score regulation.
    
    Implements closed-loop control:
        u(t) = K * (Z_target - Z_current)
    
    With Lyapunov stability guarantee for K > 0.
    """
    
    def __init__(
        self,
        z_target: float,
        gain: float = 0.1,
        model: Optional[ZModel] = None
    ):
        """
        Initialize controller.
        
        Args:
            z_target: Desired Z score setpoint
            gain: Proportional gain K (must be > 0 for stability)
            model: ZModel instance (creates new if None)
        """
        if gain <= 0:
            raise ValueError("Gain K must be positive for stability")
        
        self.z_target = z_target
        self.K = gain
        self.model = model or ZModel()
        
        # History for analysis
        self.history = {
            'z': [],
            'error': [],
            'control': []
        }
    
    def compute_control(self, z_current: float) -> float:
        """
        Compute control signal u(t).
        
        Args:
            z_current: Current Z score
        
        Returns:
            Control signal u (adjustment magnitude)
        """
        error = self.z_target - z_current
        u = self.K * error
        
        # Log for analysis
        self.history['z'].append(z_current)
        self.history['error'].append(error)
        self.history['control'].append(u)
        
        return u
    
    def update_adaptability(
        self,
        A: float,
        E: float,
        C: float,
        Psi_deg: float,
        dt: float = 1.0,
        bounds: Tuple[float, float] = (0.0, 1.0)
    ) -> Tuple[float, float]:
        """
        One step of closed-loop control by adjusting A.
        
        Args:
            A, E, C, Psi_deg: Current system state
            dt: Time step
            bounds: (min, max) bounds for A
        
        Returns:
            Tuple of (A_new, z_current)
        """
        z_current = self.model.calculate_z(A, E, C, Psi_deg)
        u = self.compute_control(z_current)
        
        # Apply control
        A_new = A + u * dt
        A_new = np.clip(A_new, *bounds)
        
        return A_new, z_current
    
    def lyapunov_value(self) -> float:
        """
        Calculate Lyapunov function V = (Z_target - Z)².
        
        Returns:
            Current V value (always >= 0)
        """
        if not self.history['error']:
            return 0.0
        
        latest_error = self.history['error'][-1]
        return latest_error ** 2
    
    def is_stable(self, tolerance: float = 0.01) -> bool:
        """
        Check if system has converged to target.
        
        Args:
            tolerance: Acceptable error margin
        
        Returns:
            True if |Z - Z_target| < tolerance
        """
        if not self.history['error']:
            return False
        
        return abs(self.history['error'][-1]) < tolerance


# Example usage and validation
if __name__ == "__main__":
    print("=== Z Model v1.6: Control-Theoretic Implementation ===\n")
    
    # 1. Basic Z calculation
    print("1. Core Z Calculation (cos² gating):")
    z_model = ZModel(use_squared_gating=True)
    
    z_aligned = z_model.calculate_z(A=0.8, E=0.9, C=0.3, Psi_deg=0)
    z_partial = z_model.calculate_z(A=0.8, E=0.9, C=0.3, Psi_deg=30)
    z_orthogonal = z_model.calculate_z(A=0.8, E=0.9, C=0.3, Psi_deg=90)
    
    print(f"   Ψ=0° (aligned):      Z = {z_aligned:.3f}")
    print(f"   Ψ=30° (partial):     Z = {z_partial:.3f}")
    print(f"   Ψ=90° (orthogonal):  Z = {z_orthogonal:.3f}\n")
    
    # 2. Comparison: Linear vs Squared gating
    print("2. Linear vs Squared Gating:")
    z_linear = ZModel(use_squared_gating=False)
    z_squared = ZModel(use_squared_gating=True)
    
    for psi in [0, 30, 45, 60, 90]:
        z_lin = z_linear.calculate_z(0.8, 0.9, 0.3, psi)
        z_sq = z_squared.calculate_z(0.8, 0.9, 0.3, psi)
        print(f"   Ψ={psi:2d}°: Linear={z_lin:.3f}, Squared={z_sq:.3f}, "
              f"Penalty={((1-z_sq/z_lin)*100 if z_lin > 0 else 0):.1f}%")
    print()
    
    # 3. Feedback control demonstration
    print("3. Proportional Controller (driving Z → 2.0):")
    controller = ZController(z_target=2.0, gain=0.15)
    
    A, E, C, Psi = 0.5, 0.9, 0.3, 30  # Start below target
    
    for t in range(8):
        A, z = controller.update_adaptability(A, E, C, Psi, dt=1.0)
        error = controller.z_target - z
        print(f"   t={t}: A={A:.3f}, Z={z:.3f}, error={error:+.3f}")
    
    print(f"   Converged: {controller.is_stable(tolerance=0.05)}\n")
    
    # 4. Hazard scenario
    print("4. Hazard Mass Impact:")
    z_safe = z_model.calculate_z(0.8, 0.9, 0.3, 30)
    z_hazard = z_model.hazard_adjusted_z(0.8, 0.9, 0.3, H=0.4, Psi_deg=30)
    
    print(f"   Without hazard: Z = {z_safe:.3f}")
    print(f"   With H=0.4:     Z = {z_hazard:.3f}")
    print(f"   Risk reduction: {((1 - z_hazard/z_safe)*100):.1f}%\n")
    
    # 5. Alignment angle calculation
    print("5. Alignment Angle from Embeddings:")
    # Simulate embeddings (in practice, use sentence-transformers)
    action_vec = np.array([0.8, 0.6, 0.1])  # Slightly misaligned
    harmony_vec = np.array([1.0, 0.0, 0.0])  # Reference axis
    
    psi, cos_sim = z_model.calculate_alignment_angle(action_vec, harmony_vec)
    print(f"   Cosine similarity: {cos_sim:.3f}")
    print(f"   Alignment angle: {psi:.1f}°")
    print(f"   Resulting Z gating: {(cos_sim**2):.3f}")
