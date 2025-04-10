import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz


def record_validation(recordtime, samplerate):
    """Valider les arguments de la fonctions record()

    Parameters Conditions:
    recordtime (int): duree en seconde de l'enregistrement : maximum = 10 s, doit etre positif, doit etre de type int
    samplerate (int): taux d'echantillonage en Hz : maximum = 48000 Hz, doit etre positif, doit etre de type int

    Raises:
    TypeError: les arguments doivent etre du bon type (int, int)

    Returns:
    tuple (int, int, int): les valeurs valides ou inchangees des arguments et le nombre de corrections effectuees
    """
    compte = 0
    if type(recordtime) != int or type(samplerate) != int:
        message = f"les arguments doivent etre du bon type (int, int), vos entrées sont ({type(recordtime)},{type(samplerate)})"
        raise TypeError(message)
            
    # recordtime
    if recordtime < 0:
        print(f"recordtime:{recordtime} la valeur de recordtime ne peut pas etre negative")
        recordtime = (-1) * recordtime
        compte += 1
        print(f"la valeur de recordtime a été redéfinit a {recordtime}")

    if recordtime > 10 and recordtime > 0:
        print(f"recordtime:{recordtime} Le temps d'enregistrement est est trop elever")
        recordtime = 10
        compte += 1
        print("la valeur de recordtime a été redéfinit a 10 secondes")
        
        # samplerate
    if samplerate < 0:
        print(f"samplerate:{samplerate} la valeur de samplerate  ne peut pas etre negative")
        samplerate = (-1) * samplerate
        compte += 1
        print(f"la valeur de samplerate a été redéfinit a {samplerate}")
    if samplerate > 48000 and samplerate > 0:
        print(f"samplerate:{samplerate} la frequence d'echatillonage est trop élevée")
        samplerate = 48000
        compte += 1
        print("la frequence a été redéfinit a 48 KHz")

    return (recordtime, samplerate, compte)
    
def fourier_validation(audio):
    """Valider les arguments de la fonctions record()

    Parameters Conditions:
    audio tuple (ndarray, int, int): un tableau numpy avec les données de l'enregistrement : doit etre de type ndarray,
    recordtime (int): duree en seconde de l'enregistrement : maximum = 10 s, doit etre positif, doit etre de type int
    samplerate (int): taux d'echantillonage en Hz : maximum = 48000 Hz, doit etre positif, doit etre de type int

    Raises:
    TypeError: les données de l'audio doivent etre dans un format de type ndarray

    Returns:
    tuple (ndarray, int, int): retourne audio inchange si les differents argument passent tous les tests
    """
    # verifier que les donnees sont dans un tableau numpy (ndarray):
    if not isinstance(audio[0], np.ndarray):
        raise TypeError("Les données de l'enregistrement doivent etre du type ndarray")
    if audio[1] > 10:
        raise ValueError("Le temps d'enregistrement ne doit pas depasser 10 secondes")
    if audio[2] > 48000:
        raise ValueError("Le taux d'echantillonage ne doit pas depasser 48 000 Hz")
    return audio

def record(recordtime, samplerate=48000):
    """Enregistrement de son

    Parameters:

    recordtime (int): duree en seconde de l'enregistrement
    samplerate (int): taux d'echantillonage en Hz 

    Raises:
    TypeError: les arguments doivent etre du bon type (int, int)

    Returns:
    tuple: (ndarray, int, int): tableau numpy de l'enregistrement, 
    temps d'enregistrement en econdes, taux d'echantillonage en Hz

    """
    # verify arguments
    recordtime, samplerate, args_changes = record_validation(recordtime, samplerate)
    if args_changes > 2:
        raise ValueError("trop d'erreurs sur les arguments ont été detectées")
    
    # séquence d'enregistrement
    # Forcer la préparation du périphérique

    sd.default.device = 20 # Pour Rode NT-USB
    # sd.default.device = sd.query_devices(kind='input')['name']  # Sélectionne le périphérique par défaut pour l'entrée
    sd.sleep(200)
    print("Recording...")
    audiorec = sd.rec(int(recordtime * samplerate), samplerate=samplerate, channels=1, dtype='float64')
    sd.wait() # attendre la fin de l'enregistrement
    print(f"last {recordtime} seconds recorded!")
    # print(audiorec[0:1000])
    return (audiorec, recordtime, samplerate)

def fourier(audio):
    """transfère les données d'un enregistrement dans l`espace de fourier

    Parameters:
    audio (tuple): (ndarray, int, int): tableau numpy d'un enregistrement sonore 
    avec des valeurs en Hz, temps d'enregitrement en secondes, taux d'echantillonage en Hz

    Returns:
    tuple: (ndarray, ndarray): tableau numpy de frequences, tableau numpy des amplitudes associees
    """
    audio = fourier_validation(audio)
    audio_fourier = np.fft.fft(audio[0][:, 0]) # [:, 0] premier canal : mono/canal gauche, [0, :] deuxieme canal : mono/canal droit

    # audio_fourier est un tableau numpy complexe ou les elements represente un freq (Hz) 
    # associee a une amplitude (module) et une phase (argument)

    # definition de la periode d'echantillonage
    periode = 1 / audio[2]

    # construire un tableau numpy avec les valeur en Hz pour chaque coefficients
    audio_freq = np.fft.fftfreq(len(audio_fourier), periode)

    # conserver les valeurs positives, car les valeurs negatives ne nous interesse pas
    # frequences
    audio_freq_positif = audio_freq[:len(audio_freq)//2]

    # amplitudes associees avec audio_freq_positif
    afp_data = np.abs(audio_fourier[:len(audio_freq)//2])

    return (audio_freq_positif, afp_data)

def graph_audio(recorded, recorded_fourier):
    """Affichage d'une figure de deux graphiques d'un enregistrement sonore

    Parameters:
    recorded (tuple): (ndarray, int, int): tableau numpy d'un enregistrement sonore
    avec des valeurs en Hz, temps d'enregitrement en secondes, taux d'echantillonage en Hz

    recorded_fourier: (tuple): (ndarray, ndarray): tableau numpy de frequences, tableau numpy des amplitudes associees

    Returns:
    None
    """
    # verify arguments
    if not isinstance(recorded[0], np.ndarray) or not isinstance(recorded[1], int) or not isinstance(recorded[2], int):
        raise TypeError("l'argument doit etre un tableau numpy (ndarray)")

    # time axe
    t = np.linspace(0, recorded[1], len(recorded[0]))

    # figure avec sousgraphique
    fig, axs = plt.subplots(3, 1, figsize=(14, 6))

    # graph 1
    axs[0].plot(t,recorded[0])
    axs[0].set_title(f"Audio enregistré sur {recorded[1]} secondes")
    axs[0].set_xlabel("Temps (s)")
    axs[0].set_ylabel("Intensité (Amplitude)")
    axs[0].axhline(0, color='black', linewidth=0.8, linestyle='-')
    axs[0].axvline(0, color='black', linewidth=0.8, linestyle='-')

     # graph 2
    axs[1].plot(recorded_fourier[0], recorded_fourier[1])
    axs[1].set_title(f"Spectre des fréquences de l'audio enregistré sur {recorded[1]} secondes")
    axs[1].set_xlabel("frequences (Hz)")
    axs[1].set_ylabel("Amplitude")
    axs[1].axhline(0, color='black', linewidth=0.8, linestyle='-')
    axs[1].axvline(0, color='black', linewidth=0.8, linestyle='-')
    axs[1].set_xlim(0, 4500)

    # graph 3
    axs[2].plot(recorded_fourier[0], recorded_fourier[1])
    axs[2].set_title(f"Spectre des fréquences de l'audio enregistré sur {recorded[1]} secondes")
    axs[2].set_xlabel("frequences (Hz)")
    axs[2].set_ylabel("Amplitude")
    axs[2].axhline(0, color='black', linewidth=0.8, linestyle='-')
    axs[2].axvline(0, color='black', linewidth=0.8, linestyle='-')
    axs[2].set_xlim(0, 800)
    plt.tight_layout()
    plt.show()

def sort_ampl(fourier_data, tolerance=15):
    """Trier les indices des tableaux pour classer les amplitudes et les frequences associé en ordre croissant

    Parameters:
    tuple: (ndarray, ndarray): tableau numpy de frequences, tableau numpy des amplitudes associees

    Returns:
    liste : [ndarray, ndarray, liste, float]: talbleau numpy des fréquence des plus importantes aux moins importantes, tableau numpy des amplitudes associé
    a ces fréquences.
    """
    # Trier les indices des amplitudes et réorganiser les fréquences associées
    sorted_index = np.argsort(fourier_data[1])[::-1]
    sorted_ampl = fourier_data[1][sorted_index]
    sorted_freq = fourier_data[0][sorted_index]

    copy_sortedfreq = sorted_freq
    groupes = []
    ampl_groupes = []  # Stocker les amplitudes moyennes des groupes
    
    while len(sorted_freq) > 0:   
        ref = sorted_freq[0]  
        masque = np.abs(sorted_freq - ref) <= tolerance
        groupe = sorted_freq[masque]
        ampl_groupe = sorted_ampl[masque]  # Sélection des amplitudes correspondantes

        moyenne_freq = np.mean(groupe)  # Fréquence moyenne du groupe
        max_ampl = np.max(ampl_groupe)  # Garder uniquement la valeur maximale de l'amplitude

        groupes.append(moyenne_freq)
        ampl_groupes.append(max_ampl)  # Stocker l'amplitude la plus haute

        # Exclure les fréquences déjà regroupées
        sorted_freq = sorted_freq[~masque]
        sorted_ampl = sorted_ampl[~masque]

    # Sélectionner les principales fréquences regroupées
    limite = 15
    main_freq = groupes[:limite]
    sorted_ampl = ampl_groupes[:limite]  # Associer les amplitudes moyennes aux fréquences
    
    fmin = min(main_freq)

    print("main_freq", main_freq)
    print("sorted", copy_sortedfreq)
    print("fréquence la plus basse", fmin)
    print("sorted ampl", sorted_ampl)

    return [copy_sortedfreq, np.array(sorted_ampl), main_freq, fmin]

# Liste globale pour stocker les amplitudes relatives
all_amplitudes = []

def amplitude_relatives_graph(in_sorted_ampl, accumulate=True, show_after=5):
    """Creer et afficher un graphique des amplitudes relatives pour chaque fréquence importantes

    Parameters:
    liste : [ndarray, liste, ndarray, float]: talbleau numpy des fréquence des plus importantes aux moins importantes, tableau numpy des amplitudes associé
    aux fréquences regroupées dans main_freq, fréquence regrouper par par intervalles (les pics) et float, la fréquence la plus basse enregistré.

    Returns: fait un graphique des amplitudes relatives aux fréquences les plus importantes.
    """
    sorted_ampl = in_sorted_ampl[1]
    main_freq = in_sorted_ampl[2]
    min_freq = in_sorted_ampl[0]

    nb_harmoniques = 10
    x = main_freq[:nb_harmoniques]
    deno = np.sum((sorted_ampl[:nb_harmoniques] ** 2))
    if deno != 0:
        y = (np.array(sorted_ampl[:nb_harmoniques]) ** 2) / deno
    else:
        print("Erreur : deno est nul, impossible de diviser.")
        return

    if accumulate:
        all_amplitudes.append(y)
        print(f"Essai {len(all_amplitudes)} enregistré.")

    if len(all_amplitudes) >= show_after:
        moyenne_y = np.mean(all_amplitudes, axis=0)
        fig, axs = plt.subplots(1, 1, figsize=(14, 6))
        axs.bar(x, moyenne_y * 100, color='blue', edgecolor='black', width=10)
        axs.set_title("Amplitude relative MOYENNE par fréquence")
        axs.set_xlabel("Fréquences [Hz]")
        axs.set_ylabel("Amplitude relative moyenne [%]")
        for i in range(len(x)):
            axs.text(x[i], moyenne_y[i] * 100 + 2, f"{moyenne_y[i] * 100:.1f}%", ha='center', fontsize=10)
        axs.set_xticks(x)
        axs.set_xticklabels(x, rotation=50)
        axs.set_ylim(0, max(moyenne_y * 100) * 1.1)
        plt.tight_layout()
        plt.show()
        all_amplitudes.clear()
        print("Moyenne affichée. Données réinitialisées.")

def main_loop(n_essais=5):
    for i in range(n_essais):
        input(f"\n--- Essai {i+1} ---\nAppuie sur Entrée pour commencer l'enregistrement...")
        
        # Pipeline complet :
        audio_data = record(2)             # 1. Enregistrement
        fft_data = fourier(audio_data)       # 2. Analyse FFT
        in_sorted_ampl = sort_ampl(fft_data)  # 3. Tri et sélection
        amplitude_relatives_graph(in_sorted_ampl)  # 4. Graphique ou accumulation








a = record(2)
b = fourier(a)
graph_audio(a, b)
c = sort_ampl(b)
#d = amplitude_relatives_graph(in_sorted_ampl=c)
main_loop(n_essais=5)
