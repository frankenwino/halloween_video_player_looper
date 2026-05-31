# Workflows

## Application Startup

```mermaid
sequenceDiagram
    participant U as User
    participant CLI as argparse
    participant APP as Main Logic
    participant OMX as OMXPlayer

    U->>CLI: python app/halloween_video_player_looper.py [flags]
    CLI->>APP: Parsed args (video, random, sleep, test)
    
    alt -v VIDEO specified
        APP->>APP: Validate file exists and is video
        APP->>OMX: single_video_player_looper(path)
    else -r random
        APP->>APP: generate_video_list()
        APP->>APP: random.choice(video_list)
        APP->>OMX: single_video_player_looper(random_path)
    else neither
        APP->>U: Print help, exit
    end
```

## Playback Loop

```mermaid
sequenceDiagram
    participant APP as App
    participant OMX as OMXPlayer
    participant HDMI as Display

    APP->>OMX: OMXPlayer(path, args)
    APP->>OMX: pause()
    
    loop Forever
        APP->>OMX: play()
        OMX->>HDMI: Video output
        APP->>APP: sleep(duration)
        APP->>OMX: pause()
        APP->>OMX: set_position(0.0)
        
        opt sleep_minutes > 0
            APP->>APP: sleep(60 * sleep_minutes)
        end
    end

    Note over APP: KeyboardInterrupt
    APP->>OMX: quit()
    APP->>APP: sys.exit()
```

## Video Discovery

1. Resolve video directory (CWD-relative `./video/`)
2. Check directory exists → fatal exit if not
3. Walk directory tree recursively
4. For each file: check MIME type via libmagic
5. Collect files where MIME contains "video"
6. Fatal exit if list is empty
7. Return list of video paths

## Shutdown

Only mechanism: `KeyboardInterrupt` (Ctrl+C)
- Calls `player.quit()` to terminate OMXPlayer process
- Calls `sys.exit()`
