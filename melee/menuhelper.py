"""Helper functions for navigating the Melee menus in ways that would be
    cumbersome to do on your own."""
from melee import enums

"""Choose a character from the character select menu
    Intended to be called each frame while in the character select menu"""
def choosecharacter(character, ai_state, controller, swag = False):
    #Figure out where the character is on the select screen
    #NOTE: This assumes you have all characters unlocked
    #Positions will be totally wrong if something is not unlocked
    row = character.value // 9
    column = character.value % 9
    #The random slot pushes the bottom row over a slot, so compensate for that
    if row == 2:
        column = column+1
    #re-order rows so the math is simpler
    row = 2-row

    #Go to the random character
    if swag:
        row = 0
        column = 0

    #Height starts at 1, plus half a box height, plus the number of rows
    target_y = 1 + 3.5 + (row * 7.0)
    #Starts at -32.5, plus half a box width, plus the number of columns
    #NOTE: Technically, each column isn't exactly the same width, but it's close enough
    target_x = -32.5 + 3.5 + (column * 7.0)
    #Wiggle room in positioning character
    wiggleroom = 1.5

    #We want to get to a state where the cursor is NOT over the character,
    # but it's selected. Thus ensuring the token is on the character
    isOverCharacter = abs(ai_state.cursor_x - target_x) < wiggleroom and \
        abs(ai_state.cursor_y - target_y) < wiggleroom

    #Don't hold down on B, since we'll quit the menu if we do
    if controller.prev.button[enums.Button.BUTTON_B] == True:
        controller.release_button(enums.Button.BUTTON_B)
        return

    #If character is selected, and we're in of the area, and coin is down, then we're good
    if (ai_state.character == character) and ai_state.coin_down:
        controller.empty_input()
        return

    #If we're in the right area, select the character
    if isOverCharacter:
        #If we're over the character, but it isn't selected,
        #   then the coin must be somewhere else.
        #   Press B to reclaim the coin
        controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, .5)
        if (ai_state.character != character) and (ai_state.coin_down):
            controller.press_button(enums.Button.BUTTON_B)
            return
        #Press A to select our character
        else:
            if controller.prev.button[enums.Button.BUTTON_A] == False:
                controller.press_button(enums.Button.BUTTON_A)
                return
            else:
                controller.release_button(enums.Button.BUTTON_A)
                return
    else:
        #Move in
        controller.release_button(enums.Button.BUTTON_A)
        #Move up if we're too low
        if ai_state.cursor_y < target_y - wiggleroom:
            controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 1)
            return
        #Move downn if we're too high
        if ai_state.cursor_y > target_y + wiggleroom:
            controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 0)
            return
        #Move right if we're too left
        if ai_state.cursor_x < target_x - wiggleroom:
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 1, .5)
            return
        #Move left if we're too right
        if ai_state.cursor_x > target_x + wiggleroom:
            controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, .5)
            return
    controller.empty_input()

"""Choose a stage from the stage select menu
    Intended to be called each frame while in the stage select menu"""
def choosestage(stage, gamestate, controller):
    target_x, target_y = 0,0
    if stage == enums.Stage.BATTLEFIELD:
        target_x, target_y = 1,-9
    if stage == enums.Stage.FINAL_DESTINATION:
        target_x, target_y = 6.7,-9
    if stage == enums.Stage.DREAMLAND:
        target_x, target_y = 12.5,-9
    if stage == enums.Stage.POKEMON_STADIUM:
        target_x, target_y = 15, 3.5
    if stage == enums.Stage.YOSHIS_STORY:
        target_x, target_y = 3.5, 15.5
    if stage == enums.Stage.FOUNTAIN_OF_DREAMS:
        target_x, target_y = 10, 15.5
    if stage == enums.Stage.RANDOM_STAGE:
        target_x, target_y = -13.5, 3.5

    #Wiggle room in positioning cursor
    wiggleroom = 1.5
    #Move up if we're too low
    if gamestate.stage_select_cursor_y < target_y - wiggleroom:
        controller.release_button(enums.Button.BUTTON_A)
        controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 1)
        return
    #Move downn if we're too high
    if gamestate.stage_select_cursor_y > target_y + wiggleroom:
        controller.release_button(enums.Button.BUTTON_A)
        controller.tilt_analog(enums.Button.BUTTON_MAIN, .5, 0)
        return
    #Move right if we're too left
    if gamestate.stage_select_cursor_x < target_x - wiggleroom:
        controller.release_button(enums.Button.BUTTON_A)
        controller.tilt_analog(enums.Button.BUTTON_MAIN, 1, .5)
        return
    #Move left if we're too right
    if gamestate.stage_select_cursor_x > target_x + wiggleroom:
        controller.release_button(enums.Button.BUTTON_A)
        controller.tilt_analog(enums.Button.BUTTON_MAIN, 0, .5)
        return

    #If we get in the right area, press A
    controller.press_button(enums.Button.BUTTON_A)

"""Spam the start button"""
def skippostgame(controller):
    #Alternate pressing start and letting go
    if controller.prev.button[enums.Button.BUTTON_START] == False:
        controller.press_button(enums.Button.BUTTON_START)
    else:
        controller.release_button(enums.Button.BUTTON_START)
