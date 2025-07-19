class State:
    # lazy implementation of disjoint set
    # all utils are disjoint sets so this _should_ work
    def __init__(self, name, transitions, terminal=False):
        self.name = name
        self.terminal = terminal
        self.transitions = set()
        self.disjoint_sets = transitions
        self.parent_map = {}
        for transition in transitions:
            self.transitions |= transition[1]
            for element in transition[1]:
                self.parent_map[element] = transition[0]
    def find_parent(self, element):
        return self.parent_map.get(element, None)
            
    def __repr__(self):
        return self.name  + "-> " + "".join([t[0] + ", " for t in self.disjoint_sets])
class Styler:
    # tailwind utils
    colors = ["colors",{"red", "orange", "amber", "yellow",
        "lime", "green", "emerald", 
        "teal", "cyan", "sky", "blue",
        "indigo", "violet", "purple", 
        "fuchsia", "pink", "rose",
        "slate", "gray", "zinc", "neutral", "stone"}]
    shade = ["shades", {"50","100","200","300","400","500", "600","700","800", "900", "950"}]
    sides = ["sides", {"l", "r", "b", "t"}]
    positions = ["positions",{"center", "left", "right"}]
    axis = ["axis",{"x", "y"}]
    discrete_sizes = ["d_sizes", {"sm", "md", "xl", "2xl"}]
    continouous_sizes = ["c_sizes", {"2", "4", "8"}]
    roots = ["roots", {"text", "bg", "border"}]
    # define states
    states = {"roots": State("root", [roots]),
              "text": State("text", [colors, positions]),
              "colors": State("colors", [shade]),
              "shades": State("shades", set(), terminal=True),
              "positions": State("positions", set(), terminal=True)}
    def __init__(self):
        pass
    def parse_style(self, args):
        styles = args.split()
        start = Styler.states["roots"]
        valid_styles = ""
        print 
        for style in styles:
            terms = style.split("-")
            if terms[0] not in start.transitions:
                print("Bad start")
                continue
            curr_state = Styler.states[terms[0]]
            for term in terms[1:]:
                print("Curr",curr_state)
                print(term, "||", curr_state.transitions)
                if (term in curr_state.transitions):
                    next_state = curr_state.find_parent(term)
                    print("Next" , next_state)
                    curr_state = Styler.states[next_state]
                else:
                    print(style," is NOT TAILWIND")
                    break
            if curr_state.terminal:
                valid_styles += f" {style} "
            else:
                print(style, "ended on nonterminal")
        return valid_styles
            


if __name__ == "__main__":
    s = Styler()
    print(s.parse_style("text-left text-red-500"))

                     
