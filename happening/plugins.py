""" Plugin registration. """

plugin_blocks = {}


def plugin_block(key):
    """ Register a plugin block for the given key. """
    def inner_plugin_block(callback):
        if key not in plugin_blocks:
            plugin_blocks[key] = []
        plugin_blocks[key].append(callback)
        return callback
    return inner_plugin_block
