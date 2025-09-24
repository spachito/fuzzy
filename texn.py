import numpy as np
import matplotlib.pyplot as plt

# --------------------------- Fuzzy Sets ---------------------------

# Default fuzzy sets (προκαθορισμένα σύνολα ασαφών τιμών για θερμοκρασία και δόση)
T_LOW_1 = {37: 0.2, 37.5: 1, 38: 0.5, 38.5: 0.2, 39: 0, 39.5: 0, 40: 0}
T_HIGH_1 = {37: 0, 37.5: 0, 38: 0.2, 38.5: 0.5, 39: 0.8, 39.5: 1, 40: 1}

D_LOW_1 = {0: 1, 2: 0.8, 5: 0.5, 8: 0.2, 10: 0}
D_HIGH_1 = {0: 0, 2: 0.2, 5: 0.5, 8: 0.8, 10: 1}

# Alternative fuzzy sets (εναλλακτικά σύνολα για πειραματισμό)
T_LOW_2 = {36.5: 1, 37: 0.8, 37.5: 0.4, 38: 0.1, 38.5: 0}
T_HIGH_2 = {38: 0, 38.5: 0.3, 39: 0.7, 39.5: 1, 40: 1}

D_LOW_2 = {0: 1, 3: 0.7, 6: 0.4, 9: 0.1, 10: 0}
D_HIGH_2 = {0: 0, 3: 0.3, 6: 0.6, 9: 0.9, 10: 1}

# --------------------------- Βοηθητικές Συναρτήσεις ---------------------------

def fuzzify(x, fuzzy_set):
    """Υπολογίζει βαθμό συμμετοχής x σε ασαφές σύνολο μέσω γραμμικής παρεμβολής"""
    keys = sorted(fuzzy_set.keys())
    for i in range(len(keys) - 1):
        x0, x1 = keys[i], keys[i + 1]
        if x0 <= x <= x1:
            y0, y1 = fuzzy_set[x0], fuzzy_set[x1]
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return 0  # Αν είναι εκτός ορίων

def inference(mu_TLOW, mu_THIGH, method, D_LOW, D_HIGH):
    """Εκτελεί ασαφή λογισμό με χρήση των βαθμών συμμετοχής θερμοκρασίας και των fuzzy sets της δόσης"""
    D_range = np.linspace(0, 10, 100)
    output = []

    for d in D_range:
        mu_dlow = fuzzify(d, D_LOW)
        mu_dhigh = fuzzify(d, D_HIGH)

        # Επιλογή μεθόδου συνδυασμού
        if method == 'min':
            result = max(min(mu_TLOW, mu_dlow), min(mu_THIGH, mu_dhigh))
        elif method == 'product':
            result = max(mu_TLOW * mu_dlow, mu_THIGH * mu_dhigh)
        else:
            raise ValueError("Μη έγκυρη μέθοδος.")
        output.append(result)

    return D_range, np.array(output)

def defuzzify(x, μ):
    """Υπολογίζει την "τραγανή" (crisp) έξοδο μέσω του κέντρου βάρους (centroid)"""
    if np.sum(μ) == 0:
        return 0
    return np.sum(x * μ) / np.sum(μ)

def plot_fuzzy_sets(T_LOW, T_HIGH, D_LOW, D_HIGH):
    """Οπτικοποίηση των fuzzy sets θερμοκρασίας και δόσης"""
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    axs[0].plot(T_LOW.keys(), T_LOW.values(), label='T_LOW', marker='o')
    axs[0].plot(T_HIGH.keys(), T_HIGH.values(), label='T_HIGH', marker='o')
    axs[0].set_title('Fuzzy Sets Θερμοκρασίας')
    axs[0].set_xlabel('Θερμοκρασία (°C)')
    axs[0].set_ylabel('Βαθμός συμμετοχής')
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(D_LOW.keys(), D_LOW.values(), label='D_LOW', marker='o')
    axs[1].plot(D_HIGH.keys(), D_HIGH.values(), label='D_HIGH', marker='o')
    axs[1].set_title('Fuzzy Sets Δόσης')
    axs[1].set_xlabel('Δόση (ml)')
    axs[1].set_ylabel('Βαθμός συμμετοχής')
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

# --------------------------- Κύρια Λειτουργία ---------------------------

def fuzzy_system():
    print("=== Ασαφές Σύστημα Ρύθμισης Φαρμακευτικής Δόσης ===")

    # Είσοδος θερμοκρασίας από τον χρήστη
    T = float(input("Δώσε θερμοκρασία ασθενούς (°C): "))

    # Επιλογή fuzzy sets
    print("\nΕπίλεξε σύνολα ασαφών μεταβλητών:")
    print("1. Default")
    print("2. Εναλλακτικά")
    set_choice = input("Επιλογή (1/2): ")

    if set_choice == '1':
        T_LOW = T_LOW_1
        T_HIGH = T_HIGH_1
        D_LOW = D_LOW_1
        D_HIGH = D_HIGH_1
    elif set_choice == '2':
        T_LOW = T_LOW_2
        T_HIGH = T_HIGH_2
        D_LOW = D_LOW_2
        D_HIGH = D_HIGH_2
    else:
        print("Μη έγκυρη επιλογή.")
        return

    # Επιλογή μεθόδου λογισμού
    print("\nΕπίλεξε τρόπο ασαφούς λογισμού:")
    print("1. Max-Min")
    print("2. Max-Product")
    method_choice = input("Επιλογή (1/2): ")

    if method_choice == '1':
        method = 'min'
    elif method_choice == '2':
        method = 'product'
    else:
        print("Μη έγκυρη επιλογή.")
        return

    # Προβολή των fuzzy sets για επιλεγμένο σύνολο
    plot_fuzzy_sets(T_LOW, T_HIGH, D_LOW, D_HIGH)

    # Υπολογισμός βαθμών συμμετοχής
    mu_TLOW = fuzzify(T, T_LOW)
    mu_THIGH = fuzzify(T, T_HIGH)

    # Εκτέλεση ασαφούς λογισμού
    D_range, D_output = inference(mu_TLOW, mu_THIGH, method, D_LOW, D_HIGH)

    # Μετατροπή σε crisp δόση (defuzzification)
    D_crisp = defuzzify(D_range, D_output)

    # Εμφάνιση αποτελεσμάτων
    print(f"\nΘερμοκρασία: {T}°C")
    print(f"Μέλος σε T_LOW: {mu_TLOW:.2f}")
    print(f"Μέλος σε T_HIGH: {mu_THIGH:.2f}")
    print(f"Προτεινόμενη δόση φαρμάκου: {D_crisp:.2f} ml")

    # Γράφημα αποτελεσμάτων
    plt.figure(figsize=(10, 6))
    plt.plot(D_range, D_output, label='Συνδυασμένη έξοδος', color='blue')
    plt.axvline(D_crisp, color='red', linestyle='--', label=f'Crisp Δόση = {D_crisp:.2f} ml')
    plt.title('Αποτελέσματα Ασαφούς Λογισμού')
    plt.xlabel('Δόση (ml)')
    plt.ylabel('Βαθμός συμμετοχής')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --------------------------- Εκκίνηση ---------------------------

if __name__ == "__main__":
    fuzzy_system()
