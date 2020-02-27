from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


'''
name	type	maximum_rabi_rate	polar_angle
Single-Qubit Driven	Primitive	63.16731	0.05671
Single-Qubit Dynamic Decoupling	CORPSE	87.00172	0.02688
Two-Qubit Parametric Drive	Gaussian	70.03844	0.09843
Mølmer-Sørensen Drive	CinBB	97.07732	0.09173
'''

class Control(models.Model):
    """Quantum control."""

    name = models.CharField(max_length=100, help_text=_('The name of the control.'))
    type = models.CharField(max_length=30, choices=settings.CONTROL_CHOICES, help_text=_('Quantum control type.'))
    maximum_rabi_rate = models.DecimalField(error_messages={"invalid_choice":"2222"},
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(0, message="min value of zero"),
                    MaxValueValidator(100)],
        help_text=_('The maximum achievable angular frequency of the Rabi cycle for a driven quantum transition. Here, this is a number between 0 and 100.'))
    polar_angle = models.DecimalField(
        max_digits=6,
        decimal_places=5,
        validators=[MinValueValidator(0),
                    MaxValueValidator(1)], 
        help_text=_('An angle measured from the z-axis on the Bloch sphere. This is a number between 0 and 1 (units of pi).'))
