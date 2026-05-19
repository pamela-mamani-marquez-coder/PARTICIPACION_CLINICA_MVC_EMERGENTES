from .medico_controller import medico_bp as medico_controller
from .paciente_controller import paciente_bp as paciente_controller
from .consulta_controller import consulta_bp as consulta_controller

__all__ = ['medico_controller', 'paciente_controller', 'consulta_controller']