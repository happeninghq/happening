"""Appearance helpers."""

THEME_SETTINGS = {
    "General": {
        "preview": """
            <div style='background: var(--BACKGROUND-COLOR);'>
                <p>This is text on the page background.</p>
                <p>This is text on the page background.</p>
            </div>
            """,
        "variables": {
            "BACKGROUND-COLOR": {
                "default": "#EEF7FE",
                "tooltip": "The background color of the whole page"
            },

            "FONT-COLOR": {
                "default": "#3C6080",
                "tooltip": "The default font color"
            },
        }
    },

    "Header": {
        "preview": """
            <header class='main-header'>
                <h2 class='main-header__heading main-header__padded'>
                    <span>
                        Header
                    </span>
                </h2>

                <div class="main-header__menu menu">
                    <ul class="menu__list inline-list">
                        <li class="menu__item
                                menu__item--with-icon main-header__padded ">
                            <a href="#" class="menu__item__icon plain-link">
                                <i class="fa fa-calendar"></i>
                            </a>
                            <a href="#" class="menu__item__text plain-link">
                                Item
                            </a>
                        </li>
                        <li class="menu__item menu__item--with-icon
                                main-header__padded menu__item--active">
                            <a href="#" class="menu__item__icon plain-link">
                                <i class="fa fa-user"></i>
                            </a>
                            <a href="#" class="menu__item__text plain-link">
                                Highlight
                            </a>
                        </li>
                        <li class="menu__item menu__item--with-icon
                                main-header__padded notification-button">
                            <a href="#" class="menu__item__icon plain-link">
                                <i class="fa fa-bell"></i>
                            </a>
                            <a href="#" class="menu__item__text plain-link">
                                Notify
                            </a>
                            <a href="#" class="notification-button__unread
                                notification-button__unread--unread
                                notifications-list-link dropdown--link">5</a>
                        </li>
                    </ul>
                </div>

                <div class="clear"></div>
            </header>
            <nav class="secondary-navigation">
                <div class="l-container">
                    <ul class="inline-list inline-list--space">
                        <li><a class="secondary-navigation__link " href="#">
                            Secondary Navigation Link
                        </a></li>
                    </ul>
                </div>
            </nav>
            """,
        "variables": {
            "HEADER-BACKGROUND-COLOR": {
                "default": "#1976D2",
                "tooltip": "The background of the overall header"
            },
            "SECONDARY-NAV-BACKGROUND-COLOR": {
                "default": "#BBDEFB",
                "tooltip": "The background of the secondary navigation bar"
            },
            "SECONDARY-NAV-COLOR": {
                "default": "#3C6080",
                "tooltip": "The text on the secondary navigation bar"
            },
            "MENU-COLOR": {
                "default": "#FFF",
                "tooltip": "The color of text and icons on the menu"
            },
            "MENU-HIGHLIGHT-BACKGROUND-COLOR": {
                "default": "#2196F3",
                "tooltip": "The background of highlighted or selected " +
                           "menu items"
            },
            "MENU-HIGHLIGHT-COLOR": {
                "default": "#FFF",
                "tooltip": "The color of text on highlighted or selected " +
                           "menu items"
            },
            "UNREAD-NOTIFICATION-BACKGROUND-COLOR": {
                "default": "#F52424",
                "tooltip": "The background of the indicator for unread " +
                           "notifications"
            },
            "UNREAD-NOTIFICATION-COLOR": {
                "default": "#FFF",
                "tooltip": "The color of text on the indicator for unread " +
                           "notifications"
            },
        }
    },

    "Blocks": {
        "variables": {
            "BLOCK-COLOR": {
                "default": "#DEEFFC",
                "tooltip": "The background color of blocks"
            },
        }
    },

    "Forms": {
        "preview": """
            <button>A button</button>
            <br /><br />
            <label class='radio'>
                <input type='radio' checked>A radio button
            </label>
            <div class="form__field">
                <div class="form__field__label">
                    <label for="text-input">Text Input</label>
                </div>
                <input type="text" value="Text Input" />
            </div>
            <div class="form__field">
                <div class="form__field__label">
                    <label for="text-area">Text Area</label>
                </div>
                <textarea>Text Area</textarea>
            </div>
            <div class="form__field">
                <div class="form__field__label">
                    <label for="toggle">Toggle</label>
                </div>
                <div class="toggle toggle--no-content">
                    <div class="toggle__item toggle__item--first toggle__item--active">
                        Going
                    </div>
                    <div class="toggle__item toggle__item--last">
                        <a href="#">Not Going</a>
                    </div>
                </div>
            </div>
            """,
        "variables": {
            "RADIO-BACKGROUND-COLOR": {
                "default": "#7FA9D2",
                "tooltip": "The background color for radio buttons"
            },
            "RADIO-COLOR": {
                "default": "#DEEFFC",
                "tooltip": "The color of the checkbox on radio buttons"
            },
            "BUTTON-BACKGROUND-COLOR": {
                "default": "#1976D2",
                "tooltip": "The background color for buttons"
            },
            "BUTTON-COLOR": {
                "default": "#FFF",
                "tooltip": "The color of text on buttons"
            },
            "TEXT-INPUT-COLOR": {
                "default": "#000",
                "tooltip": "The color of text on text inputs"
            },
            "TEXT-INPUT-BACKGROUND-COLOR": {
                "default": "#FFF",
                "tooltip": "The color of text input backgrounds"
            },
        }
    },

    "Messages": {
        "preview": """
            <div class="message-box message-box--error">
                An error message
            </div>

            <div class="message-box message-box--success">
                A success message
            </div>

            <div class="message-box">
                A message
            </div>
        """,
        "variables": {
            "MESSAGE-BACKGROUND-COLOR": {
                "default": "#DEEFFC"
            },
            "ERROR-MESSAGE-BACKGROUND-COLOR": {
                "default": "#F52424"
            },
            "SUCCESS-MESSAGE-BACKGROUND-COLOR": {
                "default": "#149A3E"
            },
        }
    }
}
