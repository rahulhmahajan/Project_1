import numpy as np
from scipy import optimize, integrate, fft
import matplotlib.pyplot as plt

# ------------------------------
# 1. Generate noisy sine data
# ------------------------------
np.random.seed(0)
x = np.linspace(0, 10, 100)
y_true = 3.0 * np.sin(1.5 * x) + 2.0
y_noisy = y_true + np.random.normal(scale=0.5, size=len(x))

# ------------------------------
# 2. Curve fitting
# ------------------------------
def model(x, amplitude, frequency, offset):
    return amplitude * np.sin(frequency * x) + offset

params, covariance = optimize.curve_fit(model, x, y_noisy, p0=[2, 1, 1])
amp, freq, offset = params

# ------------------------------
# 3. Numerical integration
# ------------------------------
area, error = integrate.quad(lambda t: model(t, *params), 0, 10)

# ------------------------------
# 4. FFT analysis
# ------------------------------
fft_vals = fft.fft(y_noisy)
fft_freq = fft.fftfreq(len(x), d=(x[1]-x[0]))

# ------------------------------
# 5. Plot everything
# ------------------------------
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Original and fitted curve
axs[0].scatter(x, y_noisy, label="Noisy Data", alpha=0.6)
axs[0].plot(x, model(x, *params), color="red", label="Fitted Curve", linewidth=2)
axs[0].set_title(f"Curve Fit: amp={amp:.2f}, freq={freq:.2f}, offset={offset:.2f}")
axs[0].legend()

# FFT spectrum
axs[1].stem(fft_freq, np.abs(fft_vals), basefmt=" ")
axs[1].set_xlim(0, 2)  # Positive frequencies
axs[1].set_title("Frequency Spectrum (FFT)")

plt.tight_layout()
plt.show()

# Print area under curve
print(f"Area under curve (0 to 10): {area:.2f} ± {error:.2e}")
