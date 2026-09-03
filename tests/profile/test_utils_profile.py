from app.shared.utils.slug import crp_treatment_to_slug, slug_treatment


def test_slug_treatment():
    # texto normal
    text = "text test"
    result = slug_treatment(text)

    assert result == "text-test"

    # texto com espaços no inicio e no fim
    text = " text test "
    result = slug_treatment(text)

    assert result == "text-test"

    # texto com multiplos espaços
    text = "text    test"
    result = slug_treatment(text)

    assert result == "text-test"

    # texto com letras maiusculas
    text = "TEXT TEST"
    result = slug_treatment(text)

    assert result == "text-test"

    # texto com acentos
    text = "téxt tẽst"
    result = slug_treatment(text)

    assert result == "text-test"

    # texto com caracteres especiais
    text = "(@#text test&*)"
    result = slug_treatment(text)

    assert result == "text-test"

    # texto com hifens duplicados
    text = "text------test"
    result = slug_treatment(text)

    assert result == "text-test"

    # texto com hifens no inicio e no fim
    text = "-text-test-"
    result = slug_treatment(text)

    assert result == "text-test"


def test_crp_treatment_to_slug():
    # crp normal
    crp = "06/123456"
    result = crp_treatment_to_slug(crp)

    assert result == "06123456"

    # crp com espaços no inicio e no fim
    crp = " 06/123456 "
    result = crp_treatment_to_slug(crp)

    assert result == "06123456"
