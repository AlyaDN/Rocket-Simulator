import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def get_float_input(prompt, default_value):
    """Kullanıcıdan sayısal girdi alır, boş bırakılırsa varsayılan değeri kullanır."""
    user_input = input(f"{prompt} [Varsayılan: {default_value}]: ").strip()
    if not user_input:
        return float(default_value)
    try:
        return float(user_input)
    except ValueError:
        print(f" Geçersiz girdi! Varsayılan değer ({default_value}) kullanılıyor.")
        return float(default_value)

def main():
    print("=" * 60)
    print("   ETKİLEŞİMLİ 2D ROKET FIRLATMA SİMÜLASYONU   ")
    print("=" * 60)
    print("Lütfen roket ve çevre parametrelerini giriniz (Varsayılan için Enter'a basınız):\n")

    # --- KULLANICI PARAMETRE GİRDİLERİ ---
    g0 = get_float_input("Yerçekimi İvmesi g0 (m/s^2) (Dünya=9.81, Mars=3.71, Ay=1.62)", 9.81)
    m_empty = get_float_input("Roketin Boş Kütlesi (kg)", 50.0)
    m_fuel = get_float_input("Başlangıç Yakıt Kütlesi (kg)", 150.0)
    thrust = get_float_input("Motor İtki Kuvveti (N)", 5000.0)
    burn_rate = get_float_input("Yakıt Tüketim Hızı (kg/s)", 5.0)
    Cd = get_float_input("Sürüklenme (Drag) Katsayısı", 0.5)
    A = get_float_input("Roket Dik Kesit Alanı (m^2)", 0.05)

    # --- SABİTLER ---
    rho0 = 1.225  # Deniz seviyesi hava yoğunluğu (kg/m^3)
    H = 8500      # Atmosfer ölçek yüksekliği (m)

    # Hesaplanan yakıt yanma süresi
    burn_time = m_fuel / burn_rate

    # --- FİZİKSEL FARK DENKLEMLERİ (ODE) ---
    def rocket_dynamics(t, y):
        altitude, velocity, fuel_mass = y
        
        # 1. Kütle hesabı
        current_fuel = max(fuel_mass, 0.0)
        total_mass = m_empty + current_fuel
        
        # 2. İtki hesabı (Yakıt bitince itki kesilir)
        current_thrust = thrust if fuel_mass > 0 else 0.0
        
        # 3. İrtifaya bağlı atmosferik yoğunluk ve sürüklenme kuvveti
        air_density = rho0 * np.exp(-max(altitude, 0) / H)
        drag = 0.5 * air_density * (velocity ** 2) * Cd * A * np.sign(velocity)
        
        # 4. Türev denklemleri
        d_altitude = velocity
        d_velocity = (current_thrust - drag - (total_mass * g0)) / total_mass
        d_fuel = -burn_rate if fuel_mass > 0 else 0.0
        
        return [d_altitude, d_velocity, d_fuel]

    # Roket yere geri düştüğünde simülasyonu sonlandıran olay
    def hit_ground_event(t, y):
        return y[0]
    
    hit_ground_event.terminal = True
    hit_ground_event.direction = -1

    # --- SİMÜLASYONU ÇALIŞTIR ---
    print("\n[+] Simülasyon hesaplanıyor...")
    y0 = [0.0, 0.0, m_fuel]  # Başlangıç durumu: [irtifa=0, hız=0, yakıt]
    t_span = (0, 600)        # Maksimum simülasyon zamanı (saniye)

    sol = solve_ivp(rocket_dynamics, t_span, y0, events=hit_ground_event, max_step=0.1)

    # --- TELEMETRİ SONUÇLARI ---
    max_alt = np.max(sol.y[0])
    max_vel = np.max(sol.y[1])
    flight_duration = sol.t[-1]

    print("\n" + "=" * 60)
    print("           UÇUŞ TELEMETRİ SONUÇLARI           ")
    print("=" * 60)
    print(f"Maksimum İrtifa (Apogee) : {max_alt:.2f} metre ({max_alt/1000:.2f} km)")
    print(f"Maksimum Hız             : {max_vel:.2f} m/s (Mach {max_vel/343:.2f})")
    print(f"Motor Kapanma Süresi     : {burn_time:.2f} saniye")
    print(f"Toplam Uçuş Süresi       : {flight_duration:.2f} saniye")
    print("=" * 60 + "\n")

    # --- GRAFİK ÇİZİMİ ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # İrtifa Grafiği
    ax1.plot(sol.t, sol.y[0], 'b-', lw=2, label="İrtifa (m)")
    ax1.axvline(x=burn_time, color='orange', linestyle='--', label=f"Motor Kapanışı ({burn_time:.1f}s)")
    ax1.set_ylabel("İrtifa [m]", fontsize=11)
    ax1.set_title("2D Roket Fırlatma Yörüngesi ve Uçuş Kinematiği", fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Hız Grafiği
    ax2.plot(sol.t, sol.y[1], 'g-', lw=2, label="Hız (m/s)")
    ax2.axvline(x=burn_time, color='orange', linestyle='--')
    ax2.set_xlabel("Uçuş Süresi [saniye]", fontsize=11)
    ax2.set_ylabel("Hız [m/s]", fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.savefig("rocket_trajectory.png", dpi=300)
    print("[+] Grafik kaydedildi: 'rocket_trajectory.png'")
    plt.show()

if __name__ == "__main__":
    main()