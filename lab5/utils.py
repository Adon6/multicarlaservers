
class Utils(object):
    """
    tools that help co-simulation
    """
    blueprint_library = []

    def get_blueprint_library_for_all(blueprint_set):
        for bp in blueprint_set:
            if bp not in blueprint_set:
                Utils.blueprint_library.append(bp)

    
