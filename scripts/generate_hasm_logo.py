try:
    from .hasm_logo import generate_hasm_logo_variants
except ImportError:
    from hasm_logo import generate_hasm_logo_variants


if __name__ == "__main__":
    generate_hasm_logo_variants()
