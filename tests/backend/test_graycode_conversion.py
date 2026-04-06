import pytest


TEST_WIDTHS = [2, 3, 4, 5, 8, 12]


def bin_to_gray(value: int) -> int:
    return value ^ (value >> 1)


def gray_to_bin(gray: int) -> int:
    out = gray
    shift = 1
    while (gray >> shift) > 0:
        out ^= gray >> shift
        shift += 1
    return out


def hamming_distance(a: int, b: int) -> int:
    return (a ^ b).bit_count()


@pytest.mark.parametrize("width", TEST_WIDTHS)
def test_bin_to_gray_formula_and_bounds(width: int) -> None:
    maxv = 1 << width
    for binary in range(maxv):
        gray = bin_to_gray(binary)
        assert gray == ((binary >> 1) ^ binary), f"formula mismatch for width={width} value={binary}"
        assert 0 <= gray < maxv, f"gray out of bounds for width={width} value={binary}: gray={gray}"


@pytest.mark.parametrize("width", TEST_WIDTHS)
def test_gray_adjacent_values_change_one_bit(width: int) -> None:
    maxv = 1 << width
    prev = bin_to_gray(0)
    for binary in range(1, maxv):
        curr = bin_to_gray(binary)
        assert hamming_distance(prev, curr) == 1, (
            f"expected one-bit transition at width={width}, transition={binary - 1}->{binary}"
        )
        prev = curr


@pytest.mark.parametrize("width", TEST_WIDTHS)
def test_gray_round_trip_decode(width: int) -> None:
    maxv = 1 << width
    for binary in range(maxv):
        gray = bin_to_gray(binary)
        decoded = gray_to_bin(gray)
        assert decoded == binary, (
            f"round-trip mismatch for width={width}: binary={binary}, gray={gray}, decoded={decoded}"
        )


@pytest.mark.parametrize("ptr_width", [2, 3, 4, 5, 8])
def test_fifo_pointer_plus_one_width_behaves_like_gray_sequence(ptr_width: int) -> None:
    width = ptr_width + 1
    maxv = 1 << width
    prev = bin_to_gray(0)
    for binary in range(1, maxv):
        curr = bin_to_gray(binary)
        assert hamming_distance(prev, curr) == 1, (
            f"pointer+1 transition should be one bit: ptr_width={ptr_width}, "
            f"transition={binary - 1}->{binary}"
        )
        prev = curr


@pytest.mark.parametrize("width", TEST_WIDTHS)
def test_gray_wrap_boundary_is_single_bit_transition(width: int) -> None:
    maxv = 1 << width
    last_gray = bin_to_gray(maxv - 1)
    zero_gray = bin_to_gray(0)
    assert hamming_distance(last_gray, zero_gray) == 1, (
        f"wrap transition must be one bit for width={width}: "
        f"{maxv - 1}->{0} produced {last_gray:b}->{zero_gray:b}"
    )
