from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QFont, QFontMetrics
import sys
import threading
import json
import time
from pynput import keyboard as pynput_keyboard
from elevenlabs.client import ElevenLabs
from playsound import playsound
import clr
import os
import pygetwindow as gw
import re
import uuid
import tempfile

client = ElevenLabs(api_key="sk_8e205fe67312966a4df4ab6859afa560aeedcad6024a37f7")  # Replace with your actual API key

steps_data = {
    "Mansion 1": [
        "Immediately mash to skip through the 4 opening cutscenes (can't mash through the \"survival horror\" text)",
        "When you gain control of Jill, un-equip the handgun, then move back into the main hall, skipping the cutscene",
        "Again try to enter the main hall, skipping the cutscene",
        "Proceed towards Barry, skipping the cutscene, and picking up the Emblem from above the fireplace",
        "Return toward main hall door, skipping cutscene along the way",
        "At main hall door attempt to use, wait for the zombie leaving cutscene, holding the Confirm button to immediately go through the door afterward",
        "Skip the cutscene and proceed up the first set of stairs, stopping at the top step and returning down to activate the cutscene. Skip it, accept the lockpick, skip the last cutscene, and return to the dining hall.",
        "Leave the dining hall through the far door and proceed toward the Arrow",
        "Simply run past the first zombine in the upstairs hallway then grab the __Arrow__.\n    - Fast: Attempt to bait the zombie past the arrow. If sleeping, fallback to safe strat.\n    - Safe: Wait for him by the arrow until you can move around him against the wall on his other side.",
        "Proceed back to the main hall, exiting out the back towards the graveyard.",
        "Proceed to the Arrow gravestone, avoiding the zombie.\n    - Note: The shirtless zombie to the left will activate if you are too close when passing the gateway toward him",
        "Examine the arrow to remove the arrowhead, then place it into the gravestone",
        "Proceed down into the crypt to retrieve the book, pulling the __Sword Key__ from its back.\n    - Fast: You only need to rotate the book until the key is facing at roughly a 45 degree angle away from you",
        "Return up the stairs to the main hall, avoiding the zombie(s)\n    - Safe: When coming back up the steps, hug the left wall (Jill's right) through the first screen transition after exiting (when you can't see the gravestone anymore), then turn up away from the camera, hopefully running around the zombie which will usually will have moved to hug the left wall with you.",
        "Proceed through lower east doorway in main hall and subsequent doors, eventually picking up the __Chemical__ outside\n    - Safe: There are herbs alongside the chemical that may be retrieved for safety",
        "Proceed toward the mansion's eastern stairwell in the direction of the lighter and whistle\n    - Fast: Run past the first two zombies and bait the third.\n    - Safe: Same as above; this is a good zombie to practice baiting, and you should be healed up to tank the hit.",
        "Proceed through the door past the third zombie, avoiding the next zombie and entering the room with the __Lighter__ and __Dog Whistle__, grabbing them in that order.\n    - Fast: Run to the left of this zombie which usually avoids a bite though there is rare RNG where he will unavoidably bite.\n    - Safe: Same as above or attempt a bait.",
        "Leave the lighter/whistle room from the door entered and avoid the two zombies.\n    - Fast: Attempt to avoid the first same as before, and again there is rare unavoidable bite RNG. At the second zombie, run through hugging the right wall hoping for good RNG, or pause briefly at the camera transition to orient and attempt to avoid.\n    - Safe: Same as above, but definitely pause for the second zombie.\n    - Note: If you spend too long in this room, a zombie will break in from the eastern stairwell doorway, significantly complicating later traversal through this hallway.",
        "Proceed across the upper main hall toward the dogs\n    - Safe: Grab the defense dagger in the upper dining hall on your way.\n    - Fast: Never ever pick up a defense item as the first pickup always introduces a tutorial screen that must be closed.",
        "Once outside, equip the handgun, use the whistle, then move in the upper left corner of the room, aim at the wall, and begin spamming the \"change target\" button until you aim at the dog. Kill the dog, un-quip the handgun, grab the __Dog Collar__ and leave, dropping the whistle at the door when prompted (spam confirm).\n    - Fast: Use quick shots to kill the dog as close to you as possible (this is hampered by health and aggression RNG). Getting wrist bit or knocked to the ground more than once is usually a reset.\n    - Safe: Shoot as much as you can and hope for the dog to knock you to the ground which will activate the defense dagger and should finish it off. If you end up killing the second dog, you can safely full-heal on the nearby green herbs.\n    - Note: You can pick up the collar from an oddly far distance away",
        "Proceed around the stairwell and avoid the zombie in front of the far doorway, exiting through it.\n    - Fast: Bait the zombie.\n    - Safe: Attempt a bait or try to move to his right.",
        "Proceed around the corner through the doorway past the crimson head which will now activate.\n    - Safe: Pick up the herb from the ground before the crimson head activates if needed.",
        "Pick up the __Armor Key__, open the dog collar, spin around the \"coin\", activate its back, and place it into the pedestal. Exit the room from where you entered.",
        "With the crimson alive, this is now \"Murder Hall\". Proceed to the door past where the Arrow was retrieved.\n    - Fast: Bait the first zombie if necessary while also avoiding the crimson. Bait the second zombie.\n    - Safe: Run through the first doorway in front of the crimson head instead. The crimson will always lunge at you and fail, giving ample to time to exit early and avoid the remaining two zombies. You can then run through the back of the zombie in the stairwell room, and if you're fast enough you can simply run past the zombie that breaks through the door from the dog balcony, exiting back into the upper dining hall. This loses ~10 seconds (and will mess up your auto splits if using door splits), but is much safer than attempting murder hall while still learning how to bait.",
        "Enter back into the main hall, traveling around the southern walkway to the armor key door leading to the __Grenade Launcher__.\n    - Safe: There is a defense dagger on the bench after getting the grenade launcher that is elevated enough to be quickly grabbed.",
        "After getting the grenade launcher, return to the main hall and then back to the hallway leading to the eastern stairwell (the other door on the upper eastern wall).",
        "Enter the first rightside doorway to Richard, skip the cutscene, close the map, and return back to the main hall",
        "Proceed across the main hall, through the upper dining, and into the western stairwell room, this time proceeding down it and through the nearby door into the save room.\n    - Safe: If you previously avoided Murder Hall through this room the extra zombie that spawned will be around the staircase banister but it is usually facing a wall and easily avoided. If the downstairs zombie is on the stairs, you can simply move around him as he will not grab.",
        "In the save room, open the box and deposit the handgun, knife, and sword key. Grab the __Serum__ from the medicine shelf and leave.\n    - Fast: The item deposting can be optimized by using the left controller bumper before each deposit to more quickly move to empty box positions.\n    - Safe: Though the First Aid Spray (FAS) in this box is enticing, it's safer to save it for later in the game. You're about to get some herbs in a couple of rooms anyway.",
        "Proceed around the downstairs hallway to the furthest door, avoiding the zombie.\n    - Fast: If you can see the zombie's hands on the left of the screen before the camera transition this usually means you're safe to simply keep running past him along the outer wall. Otherwise attempt to bait him after the transition if necessary.\n    - Safe: Stop at the camera transition to see the zombie's position and move around him. Sometimes he'll be right on the transition though and you can't avoid ]him.",
        "Proceed down the windowed hallway to the green room with the first death mask.\n    - Safe: The stun gun battery can be quickly picked up.",
        "Move in front of the water tank and use the Chemical (second item position), then mash confirm to examine the water tank and select each of the first options until the cutscene begins. Proceed to pickup __Death Mask 1__ afterward and exit the room.\n    - Fast: Angling slightly toward the mask and mashing A will allow the mask to be grabbed from a distance while moving.\n    - Safe: Grab as many green herbs as you'd like and combine them.",
        "Run past the window-breaking zombies and turn down the adjacent hall, exiting through the furthest door.",
        "Enter the dining hall through the door immediately in front of Jill, then into the the main hall.\n    - Note: Entering into the dining hall here is a notorious spot for arranged controls sending you in the wrong direction when you begin moving with the control stick. Plan accordingly.",
        "Go up the stairs and return to Richard's location. Skip the cutscene and proceed through the next door.\n    - Note: If you took too long returning to Richard on a casual run he will be dead. This doesn't hurt anything with regards to the run, but it may make your upcoming Yawn 1 fight more difficult.",
        "Turn down the hallway and enter the door past the zombie.\n    - Safe: Even of this zombie won't lunge, as long as he's hugging the left wall you can usually move around his right side safely.",
        "Proceed around the room and light the candle then immediately begin pushing the shelf. Avoid the zombie behind it if possible, grab the __Musical Score 1__, and leave the room.\n    - Fast: After finishing the shelf push, hold up and left on the dpad to slowly turn into the room behind it then backpedal as the zombie lunges to bait him. Wait for him to finish recovering if necessary before running back around him after grabbing the score. It is then optimal to leave the room around the off-camera side of the table, but if the zombie that has entered the room cannot be seen it's usually not worth the risk.\n    - Safe: There is stun gun in the shelf to the left of the candle which can be retrieved once the room is lit. The zombie behind the shelf is difficult to deal with optimally, so it's safer to have a defense item ready.",
        "Proceed back through Richard's hallway (the inner turns with the herbs are faster), down the main hall, through the dining room, and down the hallway past the zombie to the piano room.\n    - Fast: Bait the zombie if it's not sleeping. Otherwise try to squeeze to the right and pray.\n    - Safe: If the zombie is far enough to the left, it's possible to squeeze around him, but otherwise baiting or tanking is your only option.",
        "Move around to the shelf and push it to retrieve the __Musical Score 2__. Go to the piano, combine the two scores and use them to open the wall to the __Gold Emblem__.\n    - Fast: The shelf only needs about a half push to grab the score. The combined score can be used from the side of the piano. The second score should be in the 7th inventory slot with the first to its upper right in the 6th slot.",
        "After grabbing the Emblem, mash the menu button and immediately mash confirm to use the old Emblem, which should now be in the first inventory slot. Leave the room and return to the dining hall.\n    - Note: The zombie in the hallway can be easily avoiding this time by running through his back on the right side.",
        "Place the gold Emblem above the fireplace then proceed to the clock puzzle. The button inputs are:\n    1. Confirm, \u27a1\ufe0fConfirm, Confirm\n    2. Confirm, \u27a1\ufe0fConfirm, Confirm\n    3. Cancel, Confirm",
        "Grab the __Shield Key__ then proceed to the Yawn 1 room past Richard.",
        "Move toward the center of the room to activate the cutscene, then hold down-right on the control stick while mashing to skip the second cutscene, which should immediately start you toward __Death Mask 2__ in the back of the room. Grab the mask, turn and exit along the outside of the room to avoid Yawn.\n    - Safe: After grabbing the mask and moving toward the right of the nearest vertical support beam, pause and wait for Yawn if it has not moved past the left side of the beam before continuing. This guarantees that Yawn will not do the sideways head slam on you (which always poisons) while passing on the right.\n    - Note: Yawn poison can only be cured by getting more serum from the Eastern Stairwell save room. This is of course always a reset for high level runs.",
        "Return to the main eastern hallway through Richard hallway which will now have a zombie in it that is easily avoided when moving through the inner turns of this room.",
        "Proceed toward the inner double metal doors of the hallway past the zombie and into the room with the suits of armor.\n    - Note: You can pause on the camera transition with the zombie and attempt to move past the widest side of him, otherwise the only option is to bait.",
        "Push the armored statues in the order of: upper right, lower left, lower right. The upper left statue will move into place automatically and the button can then be pressed to open the gate to the jewelry box containing __Death Mask 3__ (but don't open it yet).\n    - Fast: You can activate the button from the right side.",
        "Back in the hallway, continue heading into the eastern stairwell, avoiding the zombies and entering into the save room down the stairs.\n    - Note: The first zombie can be safely ran through on the right side and the downstairs zombie can be avoided if you're fast and run around him as wide as possible.",
        "In the save room, pick up the Incendiary Shells and leave.\n    - Safe: Also pickup the FAS and either use it if you need it, or place it in the box if you don't (you're about to run out of inventory space).",
        "Exit the eastern stairwell through the downstairs door (mashing Confirm through its text) and proceed into the gallery across the hall.",
        "Flip the light on the first painting, then run around to the other side to flip the lights on the remaining two. Proceed to the final painting at the end to open the wall to __Death Mask 4__.",
        "Exit out the nearby gate into the graveyard and proceed down to the crypt to begin placing the masks from left to right:\n    1. The first mask in your inventory (4th position)\n    2. The mask in the box (5th position) (immediately mash Confirm after examining to light first button, then rotate downward to back of box to light the second)\n    3. The first mask in your inventory (4th position)\n    4. Combine the incendiary shells into the grenade launcher (4th and 3rd positions), equip it, then place the final mask (5th position) and move toward the coffin to activate the cutscene",
        "After you regain control of Jill, immediately close the gap between Jill and the elder crimson about halfway before beginning to fire, at which point a number of things can happen:\n    1. He dies in three shots without falling (best RNG)\n    2. He falls down after one or two shots, requiring that you run up to him and aim down to shoot him again and finish him.\n    3. He takes 4 shots (worst RNG) which in a high level run is a reset, but in more casual runs can be mitigated by switching back to the regular grenades to finish him, thus saving 3 incendiary shells for Plant 42.",
        "After elder crimson goes down, un-equip the grenade launcher, retrieve the __Stone and Metal Object__, and leave out through the graveyard and gallery.",
        "After exiting the gallery, avoid the zombie ahead of you and exit through the gate behind him towards the Courtyard.\n    - Fast: Bait the zombie, falling back to the safe strat if sleeping.\n    - Safe: Wait for the zombie to come out of the hallway and run around him.",
        "Run immediately toward the pedestal at the end of this outside hallway, place the Stone and Metal Object, and exit through the door. If you're fast, the dog will not pose a problem."
    ],
    "Courtyard & Residence": [
        "Move down the steps and out towards Lisa's Hut\n    - Safe: If you're holding your side, go ahead and use the FAS here.",
        "Proceed to the weather vanes and stop each of them at the same downward position relative to the screen (W for the first/red vane, N for the second/blue vane).\n    - Note: The movement of these vanes is RNG",
        "Proceed through the now unlocked gate at the end of the path, all the way to Lisa's Hut.",
        "Move to the very back of Lisa's Hut, picking up the __Square Crank__.",
        "Go to the nearby box and deposit the Armor Key and Lighter (first and second items in inventory)\n    - Fast: The item deposting can be optimized by using the ___right___ controller bumper (since left was used on the prior box) before each deposit to more quickly move to empty box positions.",
        "Proceed through the unskippable Lisa cutscene, _but do not hold movement controls at the end_.",
        "At the end of the cutscene, wait roughly half a second before running by Lisa on her right, this will avoid damage every time. Running too soon will almost always cause Lisa to hit you.",
        "Proceed back down the path away from the hut, avoiding the zombie after the stairs.\n    - Fast: If the zombie's back is toward you, run through his backside, else fallback to safe strat.\n    - Safe: You can avoid the zombie completely by running around the right side of the tree next to him.",
        "Upon returning to the storage room at Courtyard entrance, grab the FAS and proceed around the room through the double doors toward Residence.",
        "Run past the dog through the gate up the steps.",
        "Use the square crank (third item position) to lower the water and proceed around the path to the elevator.",
        "Proceed through the gate and the winding path into the Residence.",
        "Go down the hallway into the Rec Room, grabbing the __Red Book__ and exiting. The spider at the door will only rarely attack you.",
        "Shake off the tentacle on the way to Room 002 (spin control stick or dpad and mash confirm and another face button), skipping the cutscenes and entering the bathroom.\n    - Note: It's really not worth trying to push the box around to avoid the tentacle here; it does minimal damage.",
        "Grab the __001 Key__ and leave back out of the room and down the hallway\n    - Fast: If you can grab the key and leave the bathroom fast enough, the zombie will not spawn in Room 002, which saves a tiny bit of time later.",
        "Again shake off the tentacle and go into the bathroom of Room 001. Grab the __Control Room Key__ and leave.",
        "Shake off the tentacle and return to Room 002. Push the bookshelves and proceed down the ladder to the Aqua Ring.\n    - Note: If you didn't get the zombie skip, move to the left of him as you pass him to always avoid a grab.\n    - Fast: The left bookshelf can be skipped by beginning movement into it and gradually turning toward the right bookshelf, facing it right as Jill goes into the push animation causing her to catch on the very edge of its hitbox and pushing it instead.",
        "Push those boxes into the water and proceed into the shark room.\n    - Fast: The third box does not need to be pushed all the way against the wall (the final push is usually unnecessary).",
        "Proceed through the shark room, healing with the FAS if necessary.\n    - Fast: Take the middle path. This causes an almost unavoidable shark bite, but it's always the quick bite and is still faster than outside path.\n    - Safe: Take the outside path all the way to door. A shark bite or grab is still possible but less likely.",
        "Take the ladder down into the Control Room and follow the steps to drain the water:\n    1. Use the upward console\n    2. Turn and use the righthand console\n    3. Use the lefthand console\n    4. Proceed to the table and check the valve that must be turned (it's RNG; 2 is slower)\n    5. Close the indicated valve\n    6. Again use the righthand console\n    7. Use the lefthand console\n    8. Use the initial console and leave the room",
        "Proceed into the now drained shark room and around to the platform, dropping the key into the water",
        "Jump down into the water from the leftmost side of the platform and immediately run to the right past the shark, grabbing the __Gallery Key__  off screen and leaving.\n    - Safe: Simply kill the shark as intended before proceeding into the water (but honestly the fast strat is completely safe after practicing the movement a couple of times).\n    - Note: This is another notorious spot for the control stick to send you in the wrong direction in the water, which will kill you.",
        "Proceed through the gate, up the ladder, through the locked door, and back into Room 002 of the Residence.",
        "Run immediately toward the zombie and bait a lunge, then run into him, pushing him backward until you can moved around him on the left. There is opportunity for really bad RNG here, so it's advised to have either a defense item or healing available for safety in early attempts. Possible bad RNG includes:\n    1. The zombie won't lunge. Fast option is to tank the damage and continue, but if this puts you into Orange Health and you have no healing your run is effectively dead as the closest healing is in the Rec Room. Safe option is to wait for him to walk fully into the room and go around him, but this wastes 6+ seconds.\n    2. The zombie lunges, but then quick recovers and lunges again before you can get around him, grabbing you. The result is the same as the prior RNG.",
        "Use the gallery key and grab the __Insect Spray__.",
        "Return to the hallway and grab the map, using the cancel button to exit and skip the text. Use the insect spray on the hole (5th item slot).\n     - Note: How quickly the bees die here is RNG, roughly ranging 3-6 seconds.",
        "Return to the gallery and grab the __003 Key__ at the end of the hall, then proceed into Room 003.",
        "Go to the shelf and grab the white book.",
        "Open your menu, equip the grenade launcher (first slot, should have 3 incendiary shells loaded), then use the Red Book (should be 4th slot)",
        "Solve the book puzzle _(note that for books 2 and 3, it's faster to move left and grab books 6 and 7 first)_:\n    1. 1\ufe0f\u20e3\u2194\ufe0f4\ufe0f\u20e3\n    2. 2\ufe0f\u20e3\u2194\ufe0f6\ufe0f\u20e3\n    3. 3\ufe0f\u20e3\u2194\ufe0f7\ufe0f\u20e3",
        "Proceed through the door to Plant 42 and follow these steps to avoid all damage and get a quick kill:\n    1. Run four steps into the room, angling slightly to the left to avoid the staircase\n    2. Immediately turn hard to the left, running toward the angled staircase across the room\n    3. Proceed roughly 5 steps up from the turn on the staircase and aim up at P42\n    4. After it has begun to open (sound effect), fire twice, triggering the midway cutscene\n    5. Immediately aim up and quickly fire again, killing it before it closes\n    6. Open your menu, load the grenade shells into the empty launcher and un-equip it",
        "If killed fast enough, the closing and reopening animation during the P42 death cutscene can be skipped, saving time. If P42 is not killed before closing, it will start to spray poison that must be avoided before it will reopen, losing ~10 seconds.",
        "Grab the __Helmet Key__ and leave the room out the double doors",
        "Leave the Residence, proceeding back to the Mansion\n    - Safe: a Blue Herb can be quickly grabbed on the way out of the Residence which may be needed for several upcoming chances of being poisoned",
        "Upon return to the poolside path, several snakes will jump out to bite Jill. They can be avoided with a specific line that is better seen than described in text, so see a competitive run for reference. Bites have a chance to poison.",
        "Running by the dog in the next room, there is a chance for it to hit or grab you. You can attempt to avoid a grab with quick control stick movement if you see the dog going for you.\n    - Safe: If you skipped the first blue herb and were poisoned by the snakes you can use the herb here, though it is much slower to do so and risks a dog bite.",
        "Return to the Mansion.\n    - Safe: Grab the new FAS in the storage room on the way if needed/desired.\n    - Safe: Grab the new grenade shells if you're under 5 or if you're worried about the upcoming hunters."
    ],
    "Mansion 2 (Electric Boogaloo)": [
        "Proceed to the eastern stairwell room, following these steps:\n     1. Move forward until the first camera transition\n     2. Wait for the upstairs hunter to run all the way to the overhang directly above Jill and stop\n     3. As the hunter is about to scream, begin moving and stair skating up, hopefully passing the second hunter before he is able to jump to the stairs (RNG)\n     4. Backup: If you get blocked, you can optionally knock him down with the grenade launcher and attempt to continue past him (but ensure you have 5 grenades for Yawn 2).\n     5. Fast: If the upstairs hunter does his instant kill scream and lunge while you're waiting downstairs (rare RNG), you can immediately begin moving upstairs to save significant time.",
        "Proceed through the furthest door at the end of the hall, through the helmet key door and into the crusher puzzle room.",
        "Solve the puzzle and proceed down the hole, picking up the __Last Book 1__.\n    - Safe: A defense dagger can be quickly grabbed before jumping down the hole, which will come in handy for a couple of upcoming hallways.",
        "Proceed down the ladder under the gravestone. This ladder can be first-framed by holding Confirm.",
        "Continue through the hallways toward the power switch for the elevator (all spiders are easily avoided)\n    - Safe/Fast: You can get a bait for the zombie blocking the power switch by hugging the inner wall while moving towards him, then moving around his other side after he lunges. This also sets him up to be easily avoided after flipping the switch.\n    - Safe: The second zombie usually requires a bait, though sometimes he leaves a gap for you. You can grab the nearby dagger off the ground for him if needed.",
        "Proceed into the kitchen, hugging the whichever wall the zombie is closest to while moving towards him to bait a lunge, then moving around his left side to the elevator. If he's sleeping, he can sometimes be run around anyway.\n    - Fast: Entering the elevator after it reaches the basement can be first-framed by holding the button",
        "Quickly move around the corner towards the battery room, hugging the inside wall to avoid the zombie (basically 100% safe).",
        "Grab the battery and then head to Murder Hall",
        "This is Reverse Murder Hall. It sucks even worse than regular Murder Hall. Here we go:\n    1. The first zombie must be baited or tanked\n    2. Check the furthest mirror to see if the second zombie is in front of the crimson head and plan to bait\n    3. Bait the crimson head unless he swung at the second zombie, in which case run around them both\n    4. If the second zombie is past the crimson head, again plan to bait, but there's a chance to move through his back.\n    5. Proceed through the door towards Yawn 2; if you're not holding your side, you're in good shape.",
        "Enter Yawn's room and proceed around the corridor to the cutscene trigger:\n    1. Begin mashing menu while skipping the cutscene to quickly equip the grenade launcher (combine the additional grenade shells into it now if picked up)\n    2. Shoot four rounds into Yawn using pump cancel, then take the ladder down (if you can't pump cancel, shoot then move, then shoot, etc). If you miss a pump cancel, you'll likely have to move before continuing to fire or Yawn will bite you.\n    3. Close the gap towards Yawn until you see him pop out then fire once to finish him off.",
        "Grab the __Last Book 2__ and leave.",
        "Back in murder hall, take the turn in front of the crimson head through the door and into the next Helmet Key door (it's safe).",
        "Puzzle steps:\n    1. Turn off light\n    2. Grab grenade shells (if this maxes out your inventory you'll need to combine them now)\n    3. Push the drawers once toward the red gem (quickly turn around the drawers with analog to avoid the jarring camera transition)\n    4. Move away slightly to let the bird statue turn until roughly facing the center of the room (you can optimally grab the dagger on the far side of the room while waiting if needed)\n    5. Jump on the drawers from the bird wall edge and quickly grab the red gem then leave",
        "Proceed toward the main hall, moving past the hunter on the way on its left side (100% safe).",
        "Enter the lower door toward the mirror room from the main hall",
        "Avoid the zombie and grab the __Gem Box__\n    - Fast: Walk straight and begin turning with dpad at the edge of the camera transition to walk in front of him, baiting a lunge and allowing you to run right through it. Quickly correct course with control stick to grab the box. Even if he's sleeping you should still be safe.\n    - Safe: Take the turn wider and/or let him follow you to the other side of the room away from the box first. There is a dagger on the floor if needed.",
        "Exit out the back of the main hall to the graveyard, following the path all the way out to the Courtyard again. You can simply run through the hunter by hugging the wall on the left."
    ],
    "Underground": [
        "Proceed to the pool area. The snakes will again jump out, but they're easier to avoid this time. Basically hug the left edge of the pool (ladder side) and walk straight up until the snake on the left jumps, then turn left to avoid the snakes on the right and follow the rest of the path.",
        "In the waterfall area, plug the Battery into the elevator and take it back up.",
        "Wait on the dog immediately blocking you off the elevator and when it begins running, run the opposite direction that it turns (which is usually to the right). Proceed through to the pool area, avoiding the second dog as best as possible.\n    - Safe: Sometimes it's necessary to use analog to avoid the dogs when they lunge at your wrist. It wastes time but it's faster than taking a grab.\n    - Safe 2: If you have 7 or more grenades, you can equip the grenade launcher to kill the dog at the top of the elevator. It's barely slower than waiting on him to run and much safer.",
        "Use the Square Crank to fill the pool.",
        "Proceed back down to the waterfall area.\n    - Safe: At the first dog down the elevator, wait on the left of it until it begins running, then run to right around it (it should turn left).\n    - Fast: YOLO run (not recommended).",
        "Proceed down the ladder into the underground. Go through the first door, heading to the Hex Crank.",
        "In the Hex Crank hallway:\n    1. Run until the cutscene begins\n    2. Skip cutscene\n    3. Mash to pickup the __Hex Crank__\n    4. Mash to skip cutscene\n    5. Mash to confirm pickup of the crank\n    6. Proceed back down the hallway, turning on the inside of the hunter to run past it",
        "Return to the initial underground hallway with the ladder (the two new hunters can simply be run through)",
        "Proceed around the room and get in position in front of the Hex Crank slot\n    - Safe: The square crank can be quickly exchanged for the FAS from the box if not yet used. This is relatively common even in high level runs, but item positions in the rest of this guide will assume this exchange was not made.",
        "Menu in front of the hex crank slot:\n    1. Select the grenade launcher (1st position) and combine with grenade shells (5th position)\n    2. Combine the Red Gem (now 5th position) with the Gem Box (6th position) to begin the puzzle (see next step)\n    3. Once puzzle box is complete, move down into the 7th item position and use the Hex Crank",
        "Gem Box Puzzle: There isn't a consistent strat for this, and it's kind of up to personal preference. Technically, proceeding through the pieces in order is fastest, but some start with the largest piece, placing it in the bottom right. Watch some runs where people do it and practice it however you wish to get it clean when you're ready (not an early priority). Ideally, you're moving pieces on a single axis as much as you can (as opposed to two, e.g. up and right).",
        "Proceed into the next room with the boulder. Get it rolling, run out of the way, skip the cutscene, and proceed to Black Tiger.\n    - Fast: It isn't necessary to run all the way to the boulder before turning around to start the cutscene. Watch runs and play around with it to find your own visual cue.",
        "Before regaining control of Jill, begin holding right on analog to immediately run toward the web door. At this point several different things may happen:\n    1. Best RNG: Black Tiger will screech and lunge towards you. As long as you keep moving to the right of the door this can be avoided 100% of the time, leaving Black Tiger right in front of the door. Move back towards it, equip the grenade launcher and begin shooting it which will also begin removing web from the door. If you're pump canceling, you should be able to kill it before it gets off another attack, which is usually a poison spit. There will be one remaining web on the door. Aim at it and blow it off, then exit.\n    2. Slow Poison: Black Tiger will begin charging a poison (rumbling noise). Quickly equip the grenade launcher and blow off two webs with pump canceling, analog to dodge the poison which should destroy one of the webs, then continue blowing off webs and leave. It shouldn't get another attack in if you're pump canceling.\n    3. Quick Poison: Black Tiger will spit a poison without charging. This can usually be avoided if you continue running past the door, allowing it to hit the door. Equip the grenade launcher and blow off the webs. If you're pump canceling, it shouldn't get off any further attacks.",
        "If you don't need to heal after exiting the Black Tiger room, keep the grenade launcher equipped and proceed to the next room. Otherwise, heal immediately and un-equip it.\n    - Safe: There are blue herbs here if you were poisoned during Black Tiger.",
        "Position in front of the next hex crank hole and menu, un-equip the grenade launcher, and use the Hex Crank, continuing to use it two more times, exiting the menu after the final time to start the boulder cutscene.",
        "Simply run forward towards the newly revealed door to quickly avoid the boulder.",
        "Enter the room and begin the Cylinder puzzle (again, there are different strats for this with varying degrees of optimization and safety; this is the safe strat):\n    1. Push the statue up the wall 4 times\n    2. Use the hex crank\n    3. Push down once\n    4. Push towards the center spinner until it spins\n    5. Push down twice\n    6. Push towards the center spinner until it spins\n    7. Push back towards the initial wall 3 times\n    8. Push down until it locks in place and opens the __Cylinder__",
        "Grab the Cylinder and proceed back towards Black Tiger room\n    - Note: Grabbing the Cylinder is on a timer; you can simply run against the statue and mash until you grab it to save a bit of movement.",
        "If you did not kill Black Tiger, several things can happen when proceeding back through its room. It is best to already be running as you transition in, then adapt according to what Tiger does:\n    1. It _immediately_ begins a screeching long lunge: Turn downward slightly to run behind it.\n    2. It hesitates before screeching to do a close range knockdown: Use analog to dodge away from the camera to avoid it.\n    3. It starts a slow poison: Just keep running through the room.\n    4. It does a quick poison: It's really tough to avoid this. Analog and pray.",
        "Proceed towards and grab the __Cylinder Shaft__. Combine it with the Cylinder (7th and 8th slots), and use it.\n    - Note: You can optionally stop at the box on the way to clear out your inventory of the Grenade Launcher and the two Cranks, which are no longer needed (though if you have grenades left they can be backup in the Lab). This wastes time initially, but saves menu movement for the rest of the run. The rest of the guide will continue to provide item positions in menus assuming you still have these items.",
        "Enter the code: __4231__",
        "Proceed down the elevator, skipping the two back to back cutscenes.",
        "Proceed through Lisa Hallway.\n    - Fast: Run straight through Lisa on the inside of the turn.\n    - Safe: Bait a swing from Lisa and wait to proceed.\n    - Note: The movement around Lisa in these sections is one of the key strat differences between console and 120 fps. Consult console version guides for Lisa strats here if you're not playing on 120fps/PC.",
        "Push the box once to the left, and 8 times up, then activate the lift. Exit the room.",
        "Proceed back through Lisa Hall to the elevator room.\n    - Fast: It's possible to just barely squeeze by Lisa here, again taking the inside of the turn, but it is difficult. It requires hugging the wall into the turn relatively closely without dragging against it, then as soon as the camera transition for the turn is about to happen, begin turning into the turn. If done correctly, Jill will briefly get stuck before squeezing through as Lisa begins her swing.\n    - Safe: Bait a swing and wait to proceed. The camera changes suck for analog here, but they can be easily practiced.\n    - Ultra Safe: Go down the stairs first, which will spawn Lisa on the other side of the room, then run back through the side with the wall switch.",
        "Walk towards the elevator to trigger the cutscene, skip, then continue down the ladder at the end of the walkway.",
        "Push the box 9 times to the left, and then into the compactor. Activate it, grab the __Broken Flamethrower__, then leave.",
        "In Lisa hall, flip the switch next to Lisa, then place the Broken Flamethrower (7th slot) and leave.\n    - Fast: It's possible to flip the switch from around the corner by running into the wall and mashing, thus avoiding having to wait on Lisa to swing. She will begin her swing, but if done right, there will be time to run away after the switch flips.\n    - Safe: Run past Lisa the same as your first time through this hallway, flip the switch, and wait for her swing to finish before running back by her.\n    - Ultra Safe: Run along the outside wall in the cave towards Lisa, then hard turn toward the switch when you're parallel with it. This will avoid damage 100% of the time if done correctly.",
        "Proceed around the pathway to Lisa's __Jewelry Box__ and then leave up the ladder.",
        "Proceed all the way back to the Mansion.",
        "Grab the Stone and Metal Object from the pedestal before entering the Mansion."
    ],
    "Lab": [
        "Proceed to the Spencer Family Emblem room, turn on the lamp, grab the __Metal Object__, then leave.\n    - Note: The hunter will not pose a problem if you take the turn into the door quickly enough while mashing.",
        "Proceed to the Main Hall via the Gallery/Graveyard path.",
        "Proceed down the stairs to the lowest door requiring the Stone and Metal Objects.\n    - Fast: This can be optimized slightly by holding Confirm as you approach the door, triggering viewing it at the most distant point. The initial observation of the door would have to happen later regardless.",
        "Begin the menu for placing the S&MOs into the door:\n    1. Place the already completed object (7th position)\n    2. Examine the Jewelry Box (6th position)\n    3. Combine the Metal Object (7th position) with the Stone Object (6th Position) and use it\n    4. Mash through the door",
        "Proceed down the stairs to the ladder into the Altar room.",
        "Steps for Lisa fight:\n    1. Skip the cutscene, __choose NO__ to decline returning Barry's gun, then skip the final cutscene\n    2. Immediately move towards __Barry's Magnum__ and pick it up\n    3. Move up and slightly to the left until touching the coffin and wait\n    4. As soon as Lisa begins moving, begin pushing the bottom left stone off the edge\n    5. Run around behind Lisa, equip the magnum, and shoot her off the edge (should be: 1 shot to get her to ledge grab, 2 shots to get her to fall)\n    6. Un-equip the magnum and push off the remaining stones, then exit up the elevator in the back (can first-frame activate)\n    7. Note: Shooting Lisa off the edge is sometimes tricky, as her movement is still RNG even with this setup, and it's possible to fire too quick or too far away from her after she ledge grabs, negating the shots. It's best to move closer to her after she ledge grabs and not fire until she has finished her grabbing animation. You should have 3 magnum shots remaining for the Lab. Less will require backup strats. If you have zero shots remaining, you can kill Tyrant with the 6 incendiary shells found in the refueling room, but this is obviously very slow.",
        "Move to the left side of the outside fountain and open the blue book (4th position), placing the Medal of Wolf into the slot.",
        "Move around to the other side, open the red book (3rd position), and place the Medal of Eagle into the slot.",
        "Skip the cutscene and proceed down into the Lab.",
        "Go down the stairs, avoiding the zombies.",
        "Turn into the tunnel, equip the magnum (4th slot), kill the zombie, and un-equip.",
        "Proceed to the computer and enter the username __JOHN__ and password __ADA__. Open both doors, using the password __CELL__.",
        "Go back upstairs into the room with the Lab Key.\n    - Note: The zombie in front of the door can be avoided by hugging the inner wall while entering.",
        "Enter the code __8462__ into the wall console and grab the __Lab Key__ then leave.\n    - Note: Just run forward to avoid the zombie outside the door again",
        "Return downstairs, using the lab key headed towards the Fuel Canister.\n    - Safe: If you still have grenades, you can use them to kill the naked zombie on the short steps.\n    - Fast: Move head-on towards the zombie _walking_ down the stairs, which will place him in position to puke instead of grabbing, allowing you to then run around him at the base of the steps.",
        "Proceed around the path to grab the __Fuel Canister__, then exit the room where entered.\n    - Fast: Don't kill the chimera. This is risky and not recommended, but it is the only option if you left the Lisa fight with only 2 magnum rounds (unless you have grenades left).\n    - Safe: There are a couple of strats for killing the chimera. One is to shoot with the magnum before triggering the camera transition that shows him (risky as he could jump or crouch while offscreen, wasting a bullet). Second is to run around him, hopefully triggering a swing rather than a crouch or a jump, then shoot him from behind (safer but if he does jump or crouch you must adapt).",
        "Proceed back through the hallways towards the fuel room\n    - Note: The naked zombie can simply be run through if his back remains towards you, or run around.",
        "Fill the Fuel Canister\n    - Safe: If you have grenade ammo, you can kill the zombie in this room.\n    - Fast: Move straight ahead after entering this room until in front of the zombie, then analog to the right and away again quickly to bait a lunge and run around to fill the canister.",
        "Begin Filled Fuel Canister movement (4 steps running, 2 steps walking)\n    - Fast: If the zombie was left alive, immediately run through its back and out of the room, which should only require 4 steps.",
        "Proceed all the way to where the Fuel Canister was initially retrieved, counting steps and alternating running and walking to avoid exploding (game over). Step count is preserved across rooms. Step sound effects can be used as cues, but hearing 2 step sounds does not necessarily mean two full steps were counted. For instance, if a step sound played as you began walking, you must wait until the third step sound is about to play before running. Being attacked or firing a weapon will (always?) trigger the explosion.\n    - Fast: Avoid the naked stairs zombie in the same manner as before if it was left alive.",
        "After placing the canister, proceed to activate the power. The chimeras can be easily avoided along the way by running around them.",
        "Use the elevator to enter the bottom level to the Tyrant fight",
        "Skip the 3 cutscenes, equip the magnum (4th position), kill Tyrant, un-equip, grab the key from the floor, proceed to the back computer to unlock the door, then leave (this door must be mashed to open)",
        "Proceed back upstairs, up the ladder and through the final locked door to the helipad.",
        "Skip the cutscene, pick up the Fuse and place it (7th position), mashing to skip the cutscene following",
        "Pick up the Signal Rockets and use them (7th position), skip cutscene.",
        "Jill, you did a fine job."
    ]
}

all_steps = []
for section, steps in steps_data.items():
    for idx, step in enumerate(steps):
        formatted_step = f"<b>{section} - Step {idx + 1}:</b><br>{step}"
        all_steps.append(formatted_step)

try:
    with open('settings.json', 'r') as f:
        settings = json.load(f)
        current_step = settings.get('current_step', 0)
except FileNotFoundError:
    current_step = 0

total_steps = len(all_steps)
tracker_running = True
overlay_visible = True
escape_press_count = 0
escape_press_time = time.time()

pressed_keys = set()

# Load DLL directly from current directory
dll_target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ControllerStepTrigger.dll')

import System
assembly = System.Reflection.Assembly.LoadFile(dll_target_path)

from ControllerStepTrigger import ControllerListener

ControllerListener.StartListening()

def save_settings():
    with open('settings.json', 'w') as f:
        json.dump({'current_step': current_step}, f)

def speak_step(text):
    plain_text = re.sub('<[^<]+?>', '', text)
    audio_stream = client.text_to_speech.convert(
        text=plain_text,
        voice_id="sIrHnVa5IHu730oRHx9i",
        model_id="eleven_multilingual_v1",
        optimize_streaming_latency=4
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        for chunk in audio_stream:
            temp_audio_file.write(chunk)
        temp_audio_file_path = temp_audio_file.name

    playsound(temp_audio_file_path)

    try:
        os.remove(temp_audio_file_path)
    except Exception as e:
        print(f"Could not delete temporary audio file: {e}")

class OverlayWindow(QtWidgets.QWidget):
    @QtCore.pyqtSlot(int, int)
    def moveOverlay(self, x, y):
        self.move(x, y)

    @QtCore.pyqtSlot(str)
    def display_step(self, step_text):
        self.full_text = step_text
        self.current_char_index = 0
        self.fit_text_to_label(step_text)
        self.step_label.setText("")
        self.typing_timer.start(40)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.Tool
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(100, 100, 800, 300)

        layout = QtWidgets.QVBoxLayout()

        self.step_label = QtWidgets.QLabel("Press 'Z' or L3+R3 to start")
        self.step_label.setStyleSheet("font-size: 22px; color: rgb(180, 0, 0); font-weight: normal;")
        self.step_label.setWordWrap(True)
        self.step_label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        layout.addWidget(self.step_label)

        button_layout = QtWidgets.QHBoxLayout()

        self.quit_button = QtWidgets.QPushButton("Exit")
        self.quit_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                background-color: rgba(220, 0, 0, 100);
                color: white;
                padding: 5px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 50, 50, 150);
            }
        """)
        self.quit_button.clicked.connect(self.quit_program)
        button_layout.addWidget(self.quit_button)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                background-color: rgba(100, 100, 100, 100);
                color: white;
                padding: 5px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(150, 150, 150, 150);
            }
        """)
        self.save_button.clicked.connect(self.save_progress)
        button_layout.addWidget(self.save_button)

        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                background-color: rgba(0, 100, 220, 100);
                color: white;
                padding: 5px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: rgba(50, 150, 255, 150);
            }
        """)
        self.reset_button.clicked.connect(self.reset_progress)
        button_layout.addWidget(self.reset_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 100);")

        self.typing_timer = QtCore.QTimer(self)
        self.typing_timer.timeout.connect(self.type_next_character)
        self.full_text = ""
        self.current_char_index = 0

    def fit_text_to_label(self, text):
        max_font_size = 22
        min_font_size = 10
        font = self.step_label.font()
        font.setPointSize(max_font_size)
        metrics = QFontMetrics(font)

        label_height = self.step_label.height()

        while (metrics.boundingRect(0, 0, self.step_label.width(), 0, QtCore.Qt.TextFlag.TextWordWrap, text).height() > label_height) and font.pointSize() > min_font_size:
            font.setPointSize(font.pointSize() - 1)
            metrics = QFontMetrics(font)

        self.step_label.setFont(font)

    def type_next_character(self):
        if self.current_char_index < len(self.full_text):
            current_text = self.step_label.text()
            self.step_label.setText(current_text + self.full_text[self.current_char_index])
            self.current_char_index += 1
        else:
            self.typing_timer.stop()

    def save_progress(self):
        save_settings()

    def reset_progress(self):
        global current_step
        current_step = 0
        self.step_label.setText("Progress Reset. Press 'Z' or L3+R3 to start.")

    def quit_program(self):
        global tracker_running
        save_settings()
        tracker_running = False
        QtWidgets.QApplication.quit()

def advance_step(overlay):
    global current_step
    if current_step < total_steps:
        print(all_steps[current_step])
        QtCore.QMetaObject.invokeMethod(
            overlay, "display_step", QtCore.Qt.ConnectionType.QueuedConnection, QtCore.Q_ARG(str, all_steps[current_step])
        )
        speak_step(all_steps[current_step])
        current_step += 1
    else:
        speak_step("End of guide.")

def on_press(key, overlay):
    global current_step, tracker_running, escape_press_count, escape_press_time, overlay_visible

    try:
        key_name = None
        if hasattr(key, 'char') and key.char:
            key_name = key.char.lower()
        else:
            key_name = key.name.lower()

        pressed_keys.add(key_name)

        if key_name == 'z':
            advance_step(overlay)
            time.sleep(0.5)

        elif key_name == 'f13':
            advance_step(overlay)
            time.sleep(0.5)

        elif key_name == 'x':
            if current_step > 0:
                speak_step("Repeating step.")
                QtCore.QMetaObject.invokeMethod(
                    overlay, "display_step", QtCore.Qt.ConnectionType.QueuedConnection, QtCore.Q_ARG(str, all_steps[current_step - 1])
                )
            time.sleep(0.5)

        elif key_name == 'esc':
            current_time = time.time()
            if current_time - escape_press_time <= 1.0:
                escape_press_count += 1
                if escape_press_count >= 3:
                    print("Escape key pressed multiple times. Exiting...")
                    save_settings()
                    tracker_running = False
                    QtWidgets.QApplication.quit()
            else:
                escape_press_count = 1
            escape_press_time = current_time
            time.sleep(0.2)

        if {'shift', 'caps_lock', 'q'}.issubset(pressed_keys):
            overlay_visible = not overlay_visible
            QtCore.QMetaObject.invokeMethod(
                overlay, "setVisible", QtCore.Qt.ConnectionType.QueuedConnection, QtCore.Q_ARG(bool, overlay_visible)
            )
            print("Overlay visibility toggled.")
            time.sleep(0.5)

    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    try:
        key_name = None
        if hasattr(key, 'char') and key.char:
            key_name = key.char.lower()
        else:
            key_name = key.name.lower()

        pressed_keys.discard(key_name)

    except Exception as e:
        print(f"Error in on_release: {e}")

def run_tracker(overlay):
    print("Speedrun Tracker Ready: Press 'Z' or L3+R3 to advance, 'X' to repeat the current step.")
    listener = pynput_keyboard.Listener(
        on_press=lambda key: on_press(key, overlay),
        on_release=on_release
    )
    listener.start()

    while tracker_running:
        try:
            game_window = None
            for window in gw.getAllWindows():
                if "Resident Evil / biohazard" in window.title:
                    game_window = window
                    break

            if game_window:
                QtCore.QMetaObject.invokeMethod(
                    overlay, "moveOverlay", QtCore.Qt.ConnectionType.QueuedConnection,
                    QtCore.Q_ARG(int, game_window.left),
                    QtCore.Q_ARG(int, game_window.top + 30)
                )

            time.sleep(0.5)

        except Exception as e:
            print(f"Window tracking error: {e}")
            time.sleep(1)

def run_overlay():
    app = QtWidgets.QApplication(sys.argv)
    overlay = OverlayWindow()
    overlay.show()

    threading.Thread(target=run_tracker, args=(overlay,), daemon=True).start()

    sys.exit(app.exec())

if __name__ == "__main__":
    run_overlay()
