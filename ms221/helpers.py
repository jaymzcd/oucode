
#   ::   .: .,::::::   :::  ::::::::::. .,:::::: :::::::..   .::::::.
#  ,;;   ;;,;;;;''''   ;;;   `;;;```.;;;;;;;'''' ;;;;``;;;; ;;;`    `
# ,[[[,,,[[[ [[cccc    [[[    `]]nnn]]'  [[cccc   [[[,/[[[' '[==/[[[[,
# "$$$"""$$$ $$""""    $$'     $$$""     $$""""   $$$$$$c     '''    $
#  888   "88o888oo,__ o88oo,.__888o      888oo,__ 888b "88bo,88b    dP
#  MMM    YMM""""YUMMM""""YUMMMYMMMb     """"YUMMMMMMM   "W"  "YMmMY"


def filter_reals(vals):
    """
        In many cases we'll need to only consider real roots or intercepts so
        filter out any complex values when returning results
    """
    return [val for val in vals if val.is_real]


def _eval(func, x):
    """
        Evaluates the sympy function func for a given x
    """
    return func.evalf(subs={'x': x})
