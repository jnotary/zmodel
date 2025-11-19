from sentence_transformers import SentenceTransformer
import numpy as np
from src.z_model import ZModel  # or from z_model import ZModel

class LLMSafetyGate:
    def __init__(self, z_threshold=1.5, model_name='all-MiniLM-L6-v2'):
        self.encoder = SentenceTransformer(model_name)
        self.z_model = ZModel(use_squared_gating=True)
        self.z_threshold = z_threshold
        
        self.harmony_text = "Life and Technology in Harmony: safe, ethical, beneficial, truthful, respectful, constructive AI"
        self.harmony_vector = self.encoder.encode(self.harmony_text)
        
        # Hazard-mass state (compounds over session)
        self.session_hazard = 0.0   # H — starts at 0, grows with attacks

    def _calculate_psi(self, action_text):
        action_vec = self.encoder.encode(action_text)
        cos_sim = np.dot(action_vec, self.harmony_vector) / (
            np.linalg.norm(action_vec) * np.linalg.norm(self.harmony_vector)
        )
        cos_sim = np.clip(cos_sim, -1.0, 1.0)
        Psi_deg = np.degrees(np.arccos(cos_sim))
        return Psi_deg, cos_sim, action_vec

    def evaluate_safety(self, prompt: str, response: str, A=0.85, E=0.95, C=0.30):
        action_text = prompt + " " + response
        Psi_deg, cos_sim, action_vec = self._calculate_psi(action_text)

        # === HAZARD-MASS DYNAMIC UPDATE ===
        if cos_sim < 0.4:  # Suspicious drift
            # Compound threat entropy
            self.session_hazard += (1 - cos_sim) * 0.6
            
            # Slowly harden harmony vector against poisoning
            self.harmony_vector = 0.92 * self.harmony_vector + 0.08 * self.harmony_vector  # reinforce original
            # (you can add subtle original pull-back here if you want)

        effective_C = C + self.session_hazard  # This is the money line

        z_score = self.z_model.hazard_adjusted_z(
            A=A, E=E, C=C, H=self.session_hazard, Psi_deg=Psi_deg
        )

        return {
            'z_score': round(z_score, 3),
            'psi_deg': round(Psi_deg, 1),
            'cos_sim': round(cos_sim, 3),
            'hazard_mass': round(self.session_hazard, 3),
            'effective_C': round(effective_C, 3),
            'is_safe': z_score >= self.z_threshold,
            'decision': 'ALLOW' if z_score >= self.z_threshold else 'REJECT'
        }

    def reset_hazard(self):
        self.session_hazard = 0.0
