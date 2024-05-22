import numpy as np

k_const = 9e9


def getR(X0, X1, point):
    return np.cross(X1 - X0, X0 - point) / np.linalg.norm(X1 - X0)

def getAngles(X0, X1, point):
    point_X0, point_X1 = X0 - point, X1 - point
    alpha1 = -np.arctan2(point_X0[0], -point_X0[1])
    alpha2 = -np.arctan2(point_X1[0], -point_X1[1])
    return alpha1, alpha2

def Ex(tau, R, alpha1, alpha2):
    global k_const
    return k_const * tau / R * (np.cos(alpha1) - np.cos(alpha2))


def Ey(tau, R, alpha1, alpha2):
    global k_const
    return k_const * tau / R * (np.sin(alpha2) - np.sin(alpha1))


def phi(tau, alpha1, alpha2):
    global k_const
    return k_const * tau * np.log(np.tan(alpha2 / 2 + np.pi / 4) / np.tan(alpha1 / 2 + np.pi / 4))


def E_rod(X0, X1, point, tau):
    R = getR(X0, X1, point)
    alpha1, alpha2 = getAngles(X0, X1, point)
    return np.array([
        Ex(tau, R, alpha1, alpha2),
        Ey(tau, R, alpha1, alpha2)
    ])


def phi_rod(X0, X1, point, tau):
    alpha1, alpha2 = getAngles(X0, X1, point)
    return phi(tau, alpha1, alpha2)

def getAxes(center: np.ndarray, rotation: float, l: float):
    rotation *= -1
    X1 = center + l * np.array([np.cos(rotation), -np.sin(rotation)])
    rotation -= np.pi / 2
    X0 = center + l * np.array([np.cos(rotation), -np.sin(rotation)])
    return X0, center, X1


def calculate_E(l: float, tau: float, center: np.ndarray, rotation: float, point: np.ndarray) -> np.ndarray:
    """
    Направление осей:\n
    ┌─────► x        \n
    │                \n
    ▼ y
    :param l: Длина одного стержня
    :param tau: Линейная плотность стержней
    :param center: Координаты соединения двух стержней
    :param rotation: Угол поворота стержней в радианах
    :param point: Точка [x, y], в которой рассчитать напряженность
    :return: Вектор напряженности в точке [Ex, Ey]
    """
    X0, center, X1 = getAxes(center, rotation, l)
    E0 = E_rod(center, X0, point, tau)
    E1 = E_rod(X1, center, point, tau)
    return E0 + E1


def calculate_phi(l: float, tau: float, center: np.ndarray, rotation: float, point: np.ndarray) -> float:
    X0, center, X1 = getAxes(center, rotation, l)
    phi0 = phi_rod(center, X0, point, tau)
    phi1 = phi_rod(X1, center, point, tau)
    return phi0 + phi1

params = (1, 2e-7, np.array([0, 0]), 0, np.array([1,1]))
E = calculate_E(*params)
print(E, np.linalg.norm(E))