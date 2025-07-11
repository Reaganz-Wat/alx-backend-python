def outer_decorator(func):
    def outer_wrapper(*args, **kwargs):
        print("OUTER FUNCTION")
        value = "Secret from grandparents: be discipline enough to succeed like you are going to do"
        return func(value, *args, **kwargs)
    return outer_wrapper

def inner_decorator(func):
    def inner_wrapper(value, *args, **kwargs):
        print("INNER FUNCTION")
        print("Value got from outer_wrapper:", value)
        return func(*args, **kwargs)
    return inner_wrapper

# @outer_decorator
# @inner_decorator
def getName(age):
    return "Watmon" + " is " + str(age) + " years old"

# name = getName(24)
inner_wrapper = inner_decorator(getName)
outer_wrapper = outer_decorator(inner_wrapper)
print(outer_wrapper(25))
# print(name)