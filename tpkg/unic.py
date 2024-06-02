UNICODE = 1

F       = f'{0x266D:c}'  if UNICODE else 'b'        # ♭ Flat
N       = f'{0x266E:c}'  if UNICODE else ' '        #   Natural
S       = f'{0x266F:c}'  if UNICODE else '#'        # ♯ Sharp
T       = f'{0x1d11A:c}' if UNICODE else 'TrebStaf' # (Treble) Staff
X       = f'{0x1d12A:c}' if UNICODE else 'X'        # double Sharp
E       = f'{0x1d12B:c}' if UNICODE else 'bb'       # double Flat
#FB     = f'{0x2588:c}' # Full Block