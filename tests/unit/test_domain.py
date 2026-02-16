"""
Unit tests for Domain Models.
Targeting 100% coverage for domain/models.py and domain/types.py
"""
import pytest
from peru_susalud_seti.domain.models import HealthResourceTableA
from peru_susalud_seti.domain.types import Subject, Observer

def test_domain_invalid_ipress_code():
    """Verifies validation of IPRESS code length."""
    with pytest.raises(ValueError, match="debe tener 8 caracteres"):
        HealthResourceTableA(period="202602", ipress_code="123", ugipress_code="12345678", 
                             physical_consulting_rooms=0, functional_consulting_rooms=0, 
                             hospital_beds=0, total_physicians=0, serums_physicians=0, 
                             resident_physicians=0, nurses=0, dentists=0, psychologists=0, 
                             nutritionists=0, medical_technologists=0, midwives=0, 
                             pharmacists=0, support_staff=0, other_professionals=0, 
                             operative_ambulances=0)

def test_domain_negative_value():
    """Verifies validation of non-negative integers."""
    with pytest.raises(ValueError, match="no puede ser negativo"):
        HealthResourceTableA(period="202602", ipress_code="12345678", ugipress_code="12345678", 
                             physical_consulting_rooms=-1, functional_consulting_rooms=0, 
                             hospital_beds=0, total_physicians=0, serums_physicians=0, 
                             resident_physicians=0, nurses=0, dentists=0, psychologists=0, 
                             nutritionists=0, medical_technologists=0, midwives=0, 
                             pharmacists=0, support_staff=0, other_professionals=0, 
                             operative_ambulances=0)

def test_subject_detach():
    """Covers the detach method in Subject class (domain/types.py)."""
    class MockObs(Observer):
        def update(self, et, msg, data=None): pass
    
    sub = Subject()
    obs = MockObs()
    sub.attach(obs)
    sub.detach(obs)
    assert obs not in sub._observers


def test_subject_notify_execution():
    """
    Covers types.py line 29.
    Ensures the notification loop actually executes its body.
    """
    class ActiveObserver(Observer):
        def __init__(self):
            self.called = False
        def update(self, event_type, message, data=None):
            self.called = True
            
    sub = Subject()
    obs = ActiveObserver()
    sub.attach(obs)
    sub.notify("TEST", "Message")
    assert obs.called is True