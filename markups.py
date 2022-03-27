from telebot import types


def clear_markups():
    markup = types.ReplyKeyboardRemove(selective=False)
    return markup


def gen_markup_ege_type():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("📗Русский")
    item2 = types.KeyboardButton("📙Математика")
    item3 = types.KeyboardButton("📘Информатика")
    item_exit = types.KeyboardButton("🔙 назад")
    markup.add(item1, item2, item3, item_exit)
    return markup


def gen_markup_ege_27():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    i1, i13 = types.KeyboardButton("1"), types.KeyboardButton("13")
    i2, i14 = types.KeyboardButton("2"), types.KeyboardButton("14")
    i3, i15 = types.KeyboardButton("3"), types.KeyboardButton("15")
    i4, i16 = types.KeyboardButton("4"), types.KeyboardButton("16")
    i5, i17 = types.KeyboardButton("5"), types.KeyboardButton("17")
    i6, i18 = types.KeyboardButton("6"), types.KeyboardButton("18")
    i7, i19 = types.KeyboardButton("7"), types.KeyboardButton("19")
    i8, i20 = types.KeyboardButton("8"), types.KeyboardButton("20")
    i9, i21 = types.KeyboardButton("9"), types.KeyboardButton("21")
    i10, i22 = types.KeyboardButton("10"), types.KeyboardButton("22")
    i11, i23 = types.KeyboardButton("11"), types.KeyboardButton("23")
    i12, i24 = types.KeyboardButton("12"), types.KeyboardButton("24")
    i25, i26 = types.KeyboardButton("25"), types.KeyboardButton("26")
    i27 = types.KeyboardButton("27")
    item_exit = types.KeyboardButton("🔙 назад")
    markup.add(i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16,
               i17, i18, i20, i21, i22, i23, i24, i25, i26, i27, item_exit)
    return markup


def gen_markup_ege_18():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    i1, i13 = types.KeyboardButton("1"), types.KeyboardButton("13")
    i2, i14 = types.KeyboardButton("2"), types.KeyboardButton("14")
    i3, i15 = types.KeyboardButton("3"), types.KeyboardButton("15")
    i4, i16 = types.KeyboardButton("4"), types.KeyboardButton("16")
    i5, i17 = types.KeyboardButton("5"), types.KeyboardButton("17")
    i6, i18 = types.KeyboardButton("6"), types.KeyboardButton("18")
    i7 = types.KeyboardButton("7")
    i8 = types.KeyboardButton("8")
    i9 = types.KeyboardButton("9")
    i10 = types.KeyboardButton("10")
    i11 = types.KeyboardButton("11")
    i12 = types.KeyboardButton("12")
    item_exit = types.KeyboardButton("🔙 назад")
    markup.add(i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16,
               i17, i18, item_exit)
    return markup

