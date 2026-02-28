# Walkable Areas - Testing Checklist

Use this checklist to verify the walkable areas feature is working correctly.

## ✅ Pre-Testing Setup

- [ ] Feature code integrated into engine
- [ ] Example masks generated (`python create_example_mask.py`)
- [ ] At least one room has a walkable mask assigned
- [ ] Game runs without errors

## ✅ Basic Functionality Tests

### 1. Mask Loading
- [ ] Console shows "Loaded walkable mask for room..." message
- [ ] No error messages about missing mask files
- [ ] Game doesn't crash when entering room with mask

### 2. Visual Debug Mode
- [ ] Press **W** key - green overlay appears
- [ ] Green overlay matches expected walkable areas
- [ ] Press **W** again - overlay disappears
- [ ] Overlay aligns with room background

### 3. Walking on Walkable Areas
- [ ] Click on floor (white mask area) - player walks there
- [ ] Player moves smoothly to clicked position
- [ ] Player can walk around freely on walkable areas
- [ ] Walking animations play correctly

### 4. Blocked Areas
- [ ] Click on wall (black mask area) - player doesn't walk through
- [ ] Click on obstacle - player finds nearest walkable point
- [ ] Player stops at edge of walkable area
- [ ] No weird glitches or stuck positions

## ✅ Nearest Point Finding

### Test 1: Click Near Edge
- [ ] Click just outside walkable area
- [ ] Player walks to nearest valid point inside area
- [ ] Movement looks natural

### Test 2: Click Far from Walkable Area
- [ ] Click on wall far from floor
- [ ] System finds closest walkable point (within 200px)
- [ ] Player walks to that point

### Test 3: Click on Obstacle
- [ ] Click on table/furniture (non-walkable)
- [ ] Player walks to floor beside obstacle
- [ ] Player doesn't get stuck

## ✅ Integration Tests

### With Interactions
- [ ] Click on door - player walks to walkable point near door
- [ ] Click on item - player walks to item (on walkable area)
- [ ] Click on NPC - player walks to NPC location
- [ ] Interaction executes when player arrives

### With Inventory
- [ ] Inventory still works normally
- [ ] Can drag items from inventory
- [ ] Can use items on objects
- [ ] Inventory area not considered walkable

### With Dialogs
- [ ] Dialog appears when talking to NPC
- [ ] Player doesn't move during dialog
- [ ] Can answer dialog choices
- [ ] Movement resumes after dialog closes

### With Room Transitions
- [ ] Walk to door - transition to new room
- [ ] Player spawns in correct position in new room
- [ ] New room's walkable mask loads correctly
- [ ] Can walk in new room

## ✅ Edge Cases

### Multiple Rooms
- [ ] Each room can have different mask
- [ ] Switching rooms loads correct mask
- [ ] No mask conflicts between rooms

### No Mask (Backward Compatibility)
- [ ] Room without mask works normally
- [ ] Player can walk anywhere in maskless room
- [ ] Press W shows no overlay (or full overlay)
- [ ] No errors or warnings

### Invalid Mask Path
- [ ] Room with wrong mask path shows warning
- [ ] Game doesn't crash
- [ ] Room reverts to "walk anywhere" mode
- [ ] Console shows helpful error message

## ✅ Performance Tests

### Loading Time
- [ ] Masks load quickly on room entry
- [ ] No noticeable lag when loading mask
- [ ] Re-entering room uses cached mask (fast)

### Walking Performance
- [ ] No frame drops while walking
- [ ] Walkability checks don't slow game
- [ ] Nearest-point search is fast enough

### Memory
- [ ] Masks are cached (not reloaded each time)
- [ ] Multiple masks don't cause memory issues
- [ ] Game runs smoothly with many rooms

## ✅ Visual Quality

### Overlay Appearance
- [ ] Green overlay is visible but not too bright
- [ ] Overlay is semi-transparent (can see room)
- [ ] Overlay clearly shows walkable vs blocked
- [ ] Overlay edges are clean (not jagged)

### Mask Alignment
- [ ] Mask perfectly aligns with room background
- [ ] Walkable areas match visual floor
- [ ] Obstacles match visual objects
- [ ] No offset or scaling issues

## ✅ User Experience

### Intuitive Behavior
- [ ] Walking feels natural
- [ ] Nearest-point finding makes sense
- [ ] Player doesn't get stuck in corners
- [ ] Edge-walking looks smooth

### Error Handling
- [ ] Helpful console messages
- [ ] Graceful fallback when mask missing
- [ ] No cryptic error messages
- [ ] Game stays playable even with errors

## ✅ Documentation Tests

### Completeness
- [ ] All features documented
- [ ] Examples are clear
- [ ] Troubleshooting covers common issues
- [ ] Code examples work as shown

### Accuracy
- [ ] Documentation matches implementation
- [ ] Key combinations correct
- [ ] File paths correct
- [ ] Technical details accurate

## ✅ Helper Tools

### create_example_mask.py
- [ ] Script runs without errors
- [ ] Creates example_mask.png
- [ ] Creates example_mask_complex.png
- [ ] View mode displays mask correctly

### Example Masks
- [ ] example_mask.png loads in game
- [ ] example_mask_complex.png loads in game
- [ ] Masks demonstrate features clearly
- [ ] Can be used as templates

## 🐛 Bug Report Template

If you find issues, document them:

```
BUG: [Brief description]

Steps to Reproduce:
1. [First step]
2. [Second step]
3. [Third step]

Expected Behavior:
[What should happen]

Actual Behavior:
[What actually happens]

Environment:
- Room: [room name]
- Mask: [mask file path]
- Console Output: [any error messages]

Additional Notes:
[Screenshots, observations, etc.]
```

## ✅ Sign-Off Checklist

Before marking feature as complete:

- [ ] All basic functionality tests pass
- [ ] All integration tests pass
- [ ] All edge cases handled
- [ ] Performance is acceptable
- [ ] Documentation is complete
- [ ] Examples work correctly
- [ ] No known critical bugs
- [ ] Feature ready for production use

---

## Testing Notes

**Tester Name:** _______________
**Date:** _______________
**Version:** 1.0
**Result:** ☐ PASS  ☐ FAIL  ☐ NEEDS WORK

**Comments:**
```
[Add any observations, suggestions, or issues here]
```

---

## Quick Test Script

For rapid testing, try this sequence:

1. Start game
2. Press **W** to see overlay
3. Click on floor → should walk
4. Click on wall → should find nearest point
5. Click on door → should walk and transition
6. Check new room → should have its own mask
7. Press **W** again → should toggle off

If all 7 steps work, basic functionality is confirmed! ✅

---

**Happy Testing! 🧪**
