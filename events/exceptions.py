""" Event exceptions. """


class EventFinishedError(Exception):

    """ Trying to interact with an event which has already finished. """

    pass


class NoTicketsError(Exception):

    """ Trying to interact with tickets which do not exist. """

    pass


class TicketCancelledError(Exception):

    """ Trying to interact with tickets which was cancelled. """

    pass
