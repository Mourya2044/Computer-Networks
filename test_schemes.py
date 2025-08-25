"""
This script compares error detection capabilities of checksum and various CRC schemes
(CRC-8, CRC-10, CRC-16, CRC-32) using a sample binary string. It injects different types
of errors (random bit errors, burst errors, odd-number errors, and guaranteed undetectable
errors) into the data and evaluates whether each scheme can detect the corruption.

Modules required:
- checksum: Provides checksum generation and verification functions.
- crc: Provides CRC generation and verification functions, with configurable polynomials.
- injecterror: Provides functions to inject random, burst, odd-number, and undetectable errors.

Main functionalities:
- Injects random single/multi-bit errors and checks detection.
- Injects burst errors of various lengths and checks detection.
- Injects odd-number errors and checks detection.
- Injects guaranteed undetectable errors for each CRC polynomial and checks detection.
- Reports which bits were flipped and whether each scheme detected the error.

Usage:
Run the script to see a comparison of error detection for checksum and CRCs under different
error scenarios.
"""
import checksum
import crc
import injecterror

binary_string = "111100001111000000001111000011110000"
polynomials = {
    "CRC-8":  "100000111",
    "CRC-10": "11000000011",
    "CRC-16": "11000000000000101",
    "CRC-32": "100000100110000010001110110110111",
}

errors = [1, 2, 17, 20]  # burst error lengths


def show_bits_flipped(original: str, corrupted: str):
    """Return indices where bits differ (0 = rightmost/LSB)."""
    diffs = []
    for i, (a, b) in enumerate(zip(reversed(original), reversed(corrupted))):
        if a != b:
            diffs.append(i)
    return diffs


print("=== ERROR DETECTION COMPARISON ===")
print(f"Original data length: {len(binary_string)} bits")

# 1. Random single/multi-bit errors
print("\n--- RANDOM BIT ERRORS ---")
for count in [1, 2, 5]:
    err_data = injecterror.injecterror(binary_string, count)
    diffs = show_bits_flipped(binary_string, err_data)
    print(f"\nInjected {count} random errors at {diffs}")

    # checksum
    chk_data = checksum.generate_checksum(binary_string)
    chk_err = injecterror.injecterror(chk_data, count)
    print(f"[Checksum] Detected={not checksum.verify_checksum(chk_err)}")

    # CRCs
    for key, poly in polynomials.items():
        # crc.polynomial = poly
        crc_data = crc.generate_crc(binary_string, poly)
        crc_err = injecterror.injecterror(crc_data, count)
        print(f"[{key}] Detected={not crc.verify_crc(crc_err, poly)}")


# 2. Burst errors
print("\n--- BURST ERRORS ---")
for size in errors:
    print(f"\nBurst size = {size}")
    chk_data = checksum.generate_checksum(binary_string)
    chk_err = injecterror.injectbursterror(chk_data, size)
    print(f"[Checksum] Detected={not checksum.verify_checksum(chk_err)}")

    for key, poly in polynomials.items():
        # crc.polynomial = poly
        crc_data = crc.generate_crc(binary_string, poly)
        crc_err = injecterror.injectbursterror(crc_data, size)
        print(f"[{key}] Detected={not crc.verify_crc(crc_err, poly)}")


# 3. Odd-number errors
print("\n--- ODD-NUMBER ERRORS ---\n")
odd_err = injecterror.injectodderror(binary_string)
diffs = show_bits_flipped(binary_string, odd_err)
print(f"Injected odd-error at positions: {diffs}")

chk_data = checksum.generate_checksum(binary_string)
chk_err = injecterror.injectodderror(chk_data)
print(f"[Checksum] Detected={not checksum.verify_checksum(chk_err)}")

for key, poly in polynomials.items():
    # crc.polynomial = poly
    crc_data = crc.generate_crc(binary_string, poly)
    crc_err = injecterror.injectodderror(crc_data)
    print(f"[{key}] Detected={not crc.verify_crc(crc_err, poly)}")


# 4. Guaranteed undetectable errors
print("\n--- GUARANTEED UNDETECTABLE ERRORS ---\n")
for key, poly in polynomials.items():
    # crc.polynomial = poly
    crc_data = crc.generate_crc(binary_string, poly)
    undet = injecterror.undetectable_error(crc_data, poly)
    diffs = show_bits_flipped(crc_data, undet)
    detected = not crc.verify_crc(undet, poly)
    print(f"[{key}] Detected={detected}, Flipped bits={diffs}")
