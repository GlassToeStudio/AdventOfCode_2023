"""
--- Day 1: Trebuchet?! ---Something is wrong with global snow production, and
you've been selected to take a look. The Elves have even given you a map; on
it, they've used stars to mark the top fifty locations that are likely to be
having problems.

You've been doing this long enough to know that to restore snow operations, you
need to check all fifty stars by December 25th.

Collect stars by solving puzzles.  Two puzzles will be made available on each
day in the Advent calendar; the second puzzle is unlocked when you complete
the first.  Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful
enough") and where they're even sending you ("the sky") and why your map looks
mostly blank ("you sure ask a lot of questions") and hang on did you just say
the sky ("of course, where do you think snow comes from") when you realize
that the Elves are already loading you into a trebuchet ("please hold still,
we need to strap you in").

As they're making the final adjustments, they discover that their calibration
document (your puzzle input) has been amended by a very young Elf who was
apparently just excited to show off her art skills. Consequently, the Elves
are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line
originally contained a specific calibration value that the Elves now need to
recover. On each line, the calibration value can be found by combining the
first digit and the last digit (in that order) to form a single two-digit
number.

For example:
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and
77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the
calibration values?


Your puzzle answer was 53194.

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are
actually spelled out with letters: one, two, three, four, five, six, seven,
eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and
last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76.
Adding these together produces 281.

What is the sum of all of the calibration values?

"""


from io import TextIOWrapper


def format_data(in_file: TextIOWrapper) -> list[str]:
    """Return a list of str from the given text."

    Args:
        in_file (TextIOWrapper): text file

    Returns:
        list[str]: input data as list[str]
    """

    return [x.strip() for x in in_file.readlines()]


def get_digits(calibration_document):
    calibration_values = [[] for _ in range(len(calibration_document))]
    for i, line in enumerate(calibration_document):
        for val in line:
            try:
                calibration_values[i].append((int(val), line.index(val)))
                line = line.replace(val, "-", 1)
            except ValueError:
                pass
        if len(calibration_values[i]) == 0:
            calibration_values[i] = [(0, 1000), (0, -1)]
        if len(calibration_values[i]) == 1:
            calibration_values[i].append(calibration_values[i][0])

    return calibration_values


def get_words(calibration_document):
    words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    calibration_values = [[] for _ in range(len(calibration_document))]
    for i, line in enumerate(calibration_document):
        for j, word in enumerate(words):
            if word in line:
                temp_line = line
                while word in temp_line:
                    calibration_values[i].append((j + 1, temp_line.index(word)))
                    temp_line = temp_line.replace(word, "-" * len(word), 1)

        if len(calibration_values[i]) == 1:
            calibration_values[i].append(calibration_values[i][0])

    for i in range(len(calibration_values)):
        calibration_values[i].sort(key=lambda x: x[1])
        if len(calibration_values[i]) == 0:
            calibration_values[i] = [(0, 1000), (0, -1)]

    return calibration_values


def part_1(calibration_document):
    calibration_values = get_digits(calibration_document)
    return sum(
        [
            calibration_values[i][0][0] * 10 + calibration_values[i][-1][0]
            for i in range(len(calibration_values))
        ]
    )


def part_2(calibration_document):
    c_nums = get_digits(calibration_document)
    c_words = get_words(calibration_document)
    c_values = [[] for _ in range(len(calibration_document))]
    for i in range(len(calibration_document)):
        c_values[i].append(
            (
                c_nums[i][0][0]
                if c_nums[i][0][1] < c_words[i][0][1]
                else c_words[i][0][0],
                c_nums[i][-1][0]
                if c_nums[i][-1][1] > c_words[i][-1][1]
                else c_words[i][-1][0],
            )
        )

    return sum(
        [c_values[i][0][0] * 10 + c_values[i][0][1] for i in range(len(c_values))]
    )


if __name__ == "__main__":
    with open("Day_01/input.txt", "r", encoding="utf-8") as f:
        data = format_data(f)
    print(f"Part 1: {part_1(data)}")  # 53194
    print(f"Part 2: {part_2(data)}")  # 54249
