def find_sum() :
    nums = [20, 13, "the", 56]
    total = 0
    for x in nums:
        try:
            total += x
        except TypeError:
            print('Non-numeric type found in list!!')
        except ValueError:
            print('Invalid number found in the list')
        except Exception as exc:
            print(exc)
    return total

print(find_sum())

try:
    age = int(input("Enter your age: "))
    if age <18:
        raise Exception('Not allowed to vote!')
    print('vote registered')
except Exception as e:      # handles all types of exceptions
    print(e)
finally:
    print('Input taken')


# the * operator takes varying no. of positional arguments and unpacks them all into a single iterable object (tuple-immutable)
def my_sum(*args):
    result = 0
    for x in args:
        result += x
    return result

print(my_sum(1, -2, 3))

# for named arguments (positions of these arguments need not be fixed)
# keyword arguments unpacking operator **
def concatenate(x, **words):
    result = ""+x
    # Iterating over the 'words' dictionary
    for word in words.values():
        result += word
    return result

print(concatenate(b="Language", a="Python", c="Is", d="Great", e="!", x="the"))

#correct order of arguments
def my_function(a, b, *args, **kwargs):
    pass