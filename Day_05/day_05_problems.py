"""
--- Day 5: If You Give A Seed A Fertilizer ---You take the boat and find the
gardener right where you were told he would be: managing a giant "garden" that
looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow
Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with!
Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand
soon; we only turned off the water a few days... weeks... oh no." His face
sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot
to check why we stopped getting more sand! There's a ferry leaving soon that
is headed over in that direction - it's much faster than your boat. Could you
please go check it out?"

You barely have time to agree to this request when he brings up another. "While
you wait for the ferry, maybe you can help us with our food production
problem. The latest Island Island Almanac just arrived and we're having
trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted.
It also lists what type of soil to use with each kind of seed, what type of
fertilizer to use with each kind of soil, what type of water to use with each
kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on
is identified with a number, but numbers are reused by each category - that
is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55,
and 13.

The rest of the almanac contains a list of maps which describe how to convert
numbers from a source category into numbers in a destination category. That
is, the section that starts with seed-to-soil map: describes how to convert a
seed number (the source) to a soil number (the destination). This lets the
gardener and his team know which soil to use with which seeds, which water to
use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number
one by one, the maps describe entire ranges of numbers that can be converted.
Each line within a map contains three numbers: the destination range start,
the source range start, and the range length.

Consider again the example seed-to-soil map:
50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98,
and a range length of 2. This line means that the source range starts at 98
and contains two values: 98 and 99. The destination range is the same length,
but it starts at 50, so its two values are 50 and 51. With this information,
you know that seed number 98 corresponds to soil number 50 and that seed
number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48
values: 50, 51, ..., 96, 97. This corresponds to a destination range starting
at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53
corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination
number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks
like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial seed
number:


Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd
like to know the closest location that needs a seed. Using these maps, find
the lowest location number that corresponds to any of the initial seeds. To do
this, you'll need to convert each seed number through other categories until
you can find its corresponding location number. In this example, the
corresponding types are:


Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity
78, location 82.

Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity
43, location 43.

Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity
82, location 86.

Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity
35, location 35.


So, the lowest location number in this example is 35.
What is the lowest location number that corresponds to any of the initial seed
numbers?


Your puzzle answer was 382895070.The first half of this puzzle is complete! It
provides one gold star: *

--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading
the almanac, it looks like the seeds: line actually describes ranges of seed
numbers.

The values on the initial seeds: line come in pairs. Within each pair, the
first value is the start of the range and the second value is the length of
the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The
first range starts with seed number 79 and contains 14 values: 79, 80, ...,
91, 92. The second range starts with seed number 55 and contains 13 values:
55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of
27 seed numbers.

In the above example, the lowest location number can be obtained from seed
number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77,
temperature 45, humidity 46, and location 46. So, the lowest location number
is 46.

Consider all of the initial seed numbers listed in the ranges on the first line
of the almanac. What is the lowest location number that corresponds to any of
the initial seed numbers?

"""


from io import TextIOWrapper

KEYS = [
    "seeds:",
    "seed-to-soil:",
    "soil-to-fertilizer:",
    "fertilizer-to-water:",
    "water-to-light:",
    "light-to-temperature:",
    "temperature-to-humidity:",
    "humidity-to-location:",
]


def format_data(in_file: TextIOWrapper) -> list[str]:
    """Return a list of str from the given text."

    Args:
        in_file (TextIOWrapper): text file

    Returns:
        list[str]: input data as list[str]
    """
    tables = dict()
    data = [x.strip() for x in in_file.read().replace(" map", "").split()]
    for i, dat in enumerate(data):
        if ":" in dat:
            j = 1
            tables[dat] = []
            while ":" not in data[i + j]:
                if len(tables) != 1:
                    tables[dat].append([int(x) for x in data[i + j : i + j + 3]])
                    j += 3
                else:
                    tables[dat].append(int(data[i + j]))
                    j += 1
                if i + j + 1 > len(data):
                    return tables


def src_to_dest(initial, map):
    for dest, src, rng in map:
        if initial >= src and initial < src + rng:
            return dest + (initial - src)
    return initial


def seed_to_soil(seed, maps):
    return src_to_dest(seed, maps)


def soil_to_fertilizer(soil, maps):
    return src_to_dest(soil, maps)


def fertilizer_to_water(fertilizer, maps):
    return src_to_dest(fertilizer, maps)


def water_to_light(water, maps):
    return src_to_dest(water, maps)


def light_to_temperature(light, maps):
    return src_to_dest(light, maps)


def temperature_to_humidity(temp, maps):
    return src_to_dest(temp, maps)


def humidity_to_location(hum, maps):
    return src_to_dest(hum, maps)


def part_1(data):
    ans = float("inf")
    for src in data[KEYS[0]]:
        for i in range(1, len(KEYS)):
            src = src_to_dest(src, data[KEYS[i]])
        ans = min(ans, src)
    return ans


# def part_1(data):
#     ans = float("inf")
#     for seed in data[KEYS[0]]:
#         soil = seed_to_soil(seed, data[KEYS[1]])
#         fertilizer = soil_to_fertilizer(soil, data[KEYS[2]])
#         water = fertilizer_to_water(fertilizer, data[KEYS[3]])
#         light = water_to_light(water, data[KEYS[4]])
#         temp = light_to_temperature(light, data[KEYS[5]])
#         hum = temperature_to_humidity(temp, data[KEYS[6]])
#         loc = humidity_to_location(hum, data[KEYS[7]])
#         print(
#             f"{seed=}, {soil=}, {fertilizer=}, {water=}, {light=}, {temp=}, {hum=}, {loc=}"
#         )
#         ans = min(ans, loc)
#     return ans


def test(data):
    ans = float("inf")
    for i in range(0, len(data[KEYS[0]]), 2):
        begin, rng = data[KEYS[0]][i : i + 2]
        print(begin, rng)
        for j in range(rng):
            seed = begin + j
            soil = seed_to_soil(seed, data[KEYS[1]])
            fertilizer = soil_to_fertilizer(soil, data[KEYS[2]])
            water = fertilizer_to_water(fertilizer, data[KEYS[3]])
            light = water_to_light(water, data[KEYS[4]])
            temp = light_to_temperature(light, data[KEYS[5]])
            hum = temperature_to_humidity(temp, data[KEYS[6]])
            loc = humidity_to_location(hum, data[KEYS[7]])
            print(
                f"{seed=}, {soil=}, {fertilizer=}, {water=}, {light=}, {temp=}, {hum=}, {loc=}"
            )
            ans = min(ans, loc)
    return ans


def first_and_last(initial_set, map, to_check):
    #   initial;         span;         end
    # 4,088,478,806; 114,805,397 = 4,203,284,202 (must subtract 1)
    #      dest,           src,         rng          src end
    # [3,333,452,986; 2,926,455,387; 455,063,168] 3,381,518,554
    #   seeds:
    #   79 14 55 13
    #   seed-to-soil map:
    #   50 98 2
    #   52 50 48

    begin, span = initial_set
    end = begin + span - 1
    for dest, src, rng in map:
        if begin >= src and begin < src + rng:
            to_check.append(dest + (begin - src))
        if end < src + rng:
            to_check.append(span)
        if end >= src + rng:
            to_check.append(end - (src + rng))

        pass


def apply_range(R, map):
    A = []
    for dest, src, sz in map:
        src_end = src + sz
        NR = []
        while R:
            # [st                                     ed)
            #          [src       src_end]
            # [BEFORE ][INTER            ][AFTER        )
            (st, ed) = R.pop()
            # (src,sz) might cut (st,ed)
            before = (st, min(ed, src))
            inter = (max(st, src), min(src_end, ed))
            after = (max(src_end, st), ed)
            if before[1] > before[0]:
                NR.append(before)
            if inter[1] > inter[0]:
                A.append((inter[0] - src + dest, inter[1] - src + dest))
            if after[1] > after[0]:
                NR.append(after)
        R = NR
    return A + R


def part_2(data):
    ans = []
    for i in range(0, len(data[KEYS[0]]), 2):
        src = data[KEYS[0]][i : i + 2]
        src = [(src[0], src[0] + src[1])]
        print("src", src)
        for j in range(1, len(data)):
            src = apply_range(src, data[KEYS[j]])
        ans.append(min(src)[0])
    return min(ans)


if __name__ == "__main__":
    with open("Day_05/input.txt", "r", encoding="utf-8") as f:
        data = format_data(f)
        print(f"Part 1: {part_1(data)}")
        print(f"Part 2: {part_2(data)}")
