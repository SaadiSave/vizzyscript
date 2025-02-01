__all__ = ["AG1", "AG2", "AG3", "AG4", "AG5", "AG6", "AG7", "AG8", "AG9", "AG10", "AG"]


from dataclasses import dataclass


AG1 = False
AG2 = False
AG3 = False
AG4 = False
AG5 = False
AG6 = False
AG7 = False
AG8 = False
AG9 = False
AG10 = False


@dataclass
class AG:
    """
    Use if you have custom AGs or AG is dynamically computed
    """

    ag: int

    @staticmethod
    def set(n: int, val: bool): ...
