import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Параметры ZMA ---
frozen_truth = np.array([0.5, 0.5])  # Центр Кристалла (Истина)
mutation_drift = np.array([1.5, 0.8]) # Вектор ошибки (куда тянет галлюцинация)
threshold = 0.15 # Лимит Свойства 6 (Проективное Ограничение)

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.1, 1.1)
ax.set_title("ZMA: Invariant Operator Stabilization Simulation", color='white')
ax.set_facecolor('#0e1117')
fig.patch.set_facecolor('#0e1117')

# Отрисовка "Зоны Стабильности" (Кристалл)
circle = plt.Circle(frozen_truth, threshold, color='cyan', fill=True, alpha=0.1, label="Stability Zone (Ks)")
ax.add_artist(circle)

# Элементы графика
core_dot, = ax.plot([frozen_truth[0]], [frozen_truth[1]], 'go', markersize=10, label="Frozen Truth Core")
synthesis_dot, = ax.plot([], [], 'ro', markersize=8, label="Dynamic Synthesis (Drifting)")
path_line, = ax.plot([], [], 'w--', alpha=0.3)
correction_line, = ax.plot([], [], 'c-', linewidth=2, label="ZMA Damping Path")

ax.legend(loc='upper right')
ax.grid(alpha=0.1)

def update(frame):
    # Симуляция дрейфа (галлюцинации)
    current_drift = frozen_truth + mutation_drift * (frame / 50)
    
    # Расчет демпфирования (ZMA Logic)
    dist = np.linalg.norm(current_drift - frozen_truth)
    
    if dist > threshold:
        # Применяем Инвариантный Оператор
        direction = (current_drift - frozen_truth) / dist
        stabilized_pos = frozen_truth + direction * threshold
        synthesis_dot.set_data([stabilized_pos[0]], [stabilized_pos[1]])
        correction_line.set_data([frozen_truth[0], stabilized_pos[0]], [frozen_truth[1], stabilized_pos[1]])
        synthesis_dot.set_color('cyan') # Сигнал стабилизации
    else:
        synthesis_dot.set_data([current_drift[0]], [current_drift[1]])
        synthesis_dot.set_color('red')
        correction_line.set_data([frozen_truth[0], current_drift[0]], [frozen_truth[1], current_drift[1]])

    return synthesis_dot, correction_line

ani = FuncAnimation(fig, update, frames=100, interval=50, blit=True)

# Сохранение анимации (опционально, требует ffmpeg или imagemagick)
# ani.save('zma_stabilization.gif', writer='imagemagick')

plt.show()
