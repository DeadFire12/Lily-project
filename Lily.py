import subprocess
import json
import os
import shutil
from datetime import datetime


from intent_engine import understand


from personality import get_personality_prompt



from memory_manager import (

    load_memory,

    save_memory,

    remember,

    find_memory,

    forget_memory,

    forget_all,

    get_memories_by_category

)



from context_engine import (

    set_context,

    clear_context,

    get_context,

    has_context

)


# =========================================
# NEW AGENT SYSTEMS
# =========================================


from state_manager import (

    load_state,

    set_state,

    get_state,

    get_all_state

)



from goal_manager import (

    load_goals,

    save_goals,

    add_goal,

    complete_goal,

    get_goals

)



from brain import (

    think

)



from learning_manager import (

    load_learning,

    save_learning,

    learn,

    find_learning,

    get_all_learning

)


from backup_manager import (
    
    create_backup,
    
    list_backups
    
)


from tool_registry import (
    
    create_tool_manager
    
)


from tool_intent_engine import (
    
    understand_tool
    
)


from tool_chain import (
    
    ToolChain
    
)


from computer_manager import (
    
    get_system_info,
    
    get_cpu_info,
    
    get_memory_info,
    
    get_disk_info,
    
    get_computer_status,
    
    get_battery_info,
    
    get_network_info,
    
    get_user_info,
    
    get_datetime_info,
    
    launch_program,
    
    take_screenshot
    
)


from voice_manager import (
    
    speak,
    
    listen
)


from voice_assistant import (
    
    VoiceAssistant
    
)


from plugin_manager import (
    
    PluginManager
    
)


from file_manager import (
    list_files,
    search_files
)


# =========================================================
# CONFIGURATION
# =========================================================

LLAMA = r"D:\DEAD FIRE\Documents\FILES\llama.cpp-256707309faf9238c9f7e81ba197d93b91b65b86\build\bin\llama-cli.exe"

MODEL = r"D:\DEAD FIRE\Documents\FILES\llama.cpp-256707309faf9238c9f7e81ba197d93b91b65b86\models\qwen2-0_5b-instruct-q4_k_m.gguf"

MEMORY_FILE = "memory.json"

if not os.path.exists(LLAMA):
    print("Lily: llama.cpp was not found.")
    exit()


if not os.path.exists(MODEL):
    print("Lily: AI model was not found.")
    exit()


# =========================================================
# TIME
# =========================================================

def now():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# =========================================================
# YES / NO
# =========================================================

def is_yes(text):
    
    text = text.lower().strip()

    yes_words = [

        "yes",
        "yeah",
        "yep",
        "yup",
        "yea",
        "sure",
        "correct",
        "right",
        "exactly",
        "that's right",
        "thats right"
    ]

    for word in yes_words:

        if (
            text == word
            or text.startswith(word + " ")
            or text.startswith(word + ",")
            or text.startswith(word + ".")
            or text.startswith(word + "!")
        ):
            return True

    return False



def is_no(text):
    
    text = text.lower().strip()

    no_words = [

        "no",
        "nope",
        "nah",
        "incorrect",
        "wrong",
        "not anymore",
        "that's wrong",
        "thats wrong"
    ]

    for word in no_words:

        if (
            text == word
            or text.startswith(word + " ")
            or text.startswith(word + ",")
            or text.startswith(word + ".")
            or text.startswith(word + "!")
        ):
            return True

    return False



# =========================================================
# MEMORY STATE
# =========================================================

memory = load_memory()

state = load_state()

goals = load_goals()

learning = load_learning()


# =========================================================
# AGENT SYSTEMS
# =========================================================

tool_manager = create_tool_manager()


tool_chain = ToolChain(
    
    tool_manager
    
)


voice_assistant = VoiceAssistant(
    
    listen,
    
    speak
    
)


plugin_manager = PluginManager(
    os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ),
        "plugins"
    )
)

plugin_manager.load_plugins()


#==========================================================


pending_key = None

pending_value = None

waiting_memory_confirmation = False

waiting_new_value = False

waiting_clear_confirmation = False

pending_tool_confirmation = None


# =========================================================
# AI CONFIG
# =========================================================

def build_learning_prompt():
    
    if not learning:
        return ""

    instructions = ""

    for key, data in learning.items():

        value = data.get(
            "value",
            ""
        ).lower()

        # =========================================
        # SIMPLE EXPLANATIONS
        # =========================================

        if "prefer simple explanations" in value:

            instructions += """
IMPORTANT RESPONSE STYLE:
The user prefers simple explanations.

When answering:
- Use simple English.
- Use short sentences.
- Explain one idea at a time.
- Avoid unnecessary technical words.
- If you use a difficult word, explain it.
- Keep the answer reasonably short.
"""

        # =========================================
        # DETAILED EXPLANATIONS
        # =========================================

        elif "prefer detailed explanations" in value:

            instructions += """
IMPORTANT RESPONSE STYLE:
The user prefers detailed explanations.

When answering:
- Give more explanation and context.
- Break complicated ideas into steps.
- Include examples when useful.
"""

        # =========================================
        # OTHER LEARNED INFORMATION
        # =========================================

        else:

            instructions += (
                "\nLearned information about the user: "
                + data.get("value", "")
                + "\n"
            )

    return instructions


def build_system_prompt():
    
    return (
        "<|im_start|>system\n"
        +
        get_personality_prompt()
        +
        build_learning_prompt()
        +
        "\n<|im_end|>\n"
    )

conversation = ""


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    user = input(
        "You: "
    ).strip()


    if not user:

        continue


    lower = user.lower()
    
    # =========================================================
    # VOICE INPUT
    # =========================================================

    if lower == "voice mode":

        print("Lily: Voice mode activated. 🎙️❤️")

        spoken_text = listen()

        if spoken_text:

            print("You:", spoken_text)

            user = spoken_text.strip()
            lower = user.lower()

        else:

            print("Lily: I couldn't understand you.")

            continue


# =====================================================
# EXIT
# =====================================================

    if lower in [
        "exit",
        "quit",
        "bye"
    ]:

        print(
            "Lily: Goodbye, Master! ❤️"
        )

        break



# =====================================================
# LEARNING TEST
# =====================================================

    if lower.startswith("learn that "):

        statement = user[
            len("learn that "):
        ].strip()


        learn(
            learning,
            statement,
            statement
        )


        print(
            f"Lily: I'll learn that: {statement}. 🧠❤️"
        )

        continue


# =====================================================
# CLEAR MEMORY CONFIRMATION
# =====================================================

    if waiting_clear_confirmation:

        if is_yes(user):

            amount = len(memory)

            forget_all(
                memory
            )

            waiting_clear_confirmation = False

            print(
                f"Lily: Done, Master. "
                f"I forgot all {amount} memories. 🧠❤️"
            )

            continue


        elif is_no(user):

            waiting_clear_confirmation = False

            print(
                "Lily: Okay, I won't delete anything. ❤️"
            )

            continue


        else:

            print(
                "Lily: Please answer yes or no."
            )

            continue



# =====================================================
# NEW MEMORY VALUE
# =====================================================

    if waiting_new_value:

        remember(
            memory,
            pending_key,
            user
        )


        set_context(
            pending_key,
            user
        )


        print(
            f"Lily: Got it! Your {pending_key} "
            f"is now {user}. ❤️"
        )


        pending_key = None

        waiting_new_value = False

        continue



# =====================================================
# MEMORY CONFIRMATION
# =====================================================

    if waiting_memory_confirmation:


        if is_yes(user):

            print(
                f"Lily: Okay! I'll remember "
                f"your {pending_key} is "
                f"{pending_value}. ❤️"
            )

            remember(
                memory,
                pending_key,
                pending_value
            )


            set_context(
                pending_key,
                pending_value
            )


            pending_key = None

            pending_value = None

            waiting_memory_confirmation = False

            continue



        elif is_no(user):
    
            print(
                f"Lily: What is your correct "
                f"{pending_key}?"
            )

            waiting_new_value = True

            waiting_memory_confirmation = False

            continue


# =====================================================
# TOOL CONFIRMATION
# =====================================================

    if pending_tool_confirmation:

        action = pending_tool_confirmation.get(
            "action"
        )

        path = pending_tool_confirmation.get(
            "path"
        )


        # =================================================
        # USER SAID YES
        # =================================================

        if is_yes(user):


            # =============================================
            # DELETE
            # =============================================

            if action == "delete":

                try:

                    if os.path.isfile(path):

                        os.remove(path)

                        print(
                            f"Lily: Deleted {path} successfully. 🗑️"
                        )

                    elif os.path.isdir(path):

                        shutil.rmtree(path)

                        print(
                            f"Lily: Deleted the folder {path} successfully. 🗑️"
                        )

                    else:

                        print(
                            "Lily: That file or folder no longer exists."
                        )

                except Exception as e:

                    print(
                        "Lily: I couldn't delete that."
                    )

                    print(
                        "Error:",
                        e
                    )


            # =============================================
            # RESTART
            # =============================================

            elif action == "restart":

                print(
                    "Lily: Restarting your computer. 🔄"
                )

                os.system(
                    "shutdown /r /t 0"
                )


            # =============================================
            # SHUTDOWN
            # =============================================

            elif action == "shutdown":

                print(
                    "Lily: Shutting down your computer. 🔌"
                )

                os.system(
                    "shutdown /s /t 0"
                )


            pending_tool_confirmation = None

            continue


        # =================================================
        # USER SAID NO
        # =================================================

        elif is_no(user):

            action_name = {
                "delete": "delete that",
                "restart": "restart your computer",
                "shutdown": "shut down your computer"
            }.get(
                action,
                "do that"
            )

            pending_tool_confirmation = None

            print(
                f"Lily: Okay, I won't {action_name}. ❤️"
            )

            continue


        # =================================================
        # USER DID NOT ANSWER YES OR NO
        # =================================================

        else:

            print(
                "Lily: Please answer yes or no."
            )

            continue
        
        
    # =====================================================
    # IDENTITY
    # =====================================================

    cleaned = lower.replace(
        "?",
        ""
    ).strip()


    if cleaned in [

        "who are you",

        "what is your name",

        "whats your name",

        "what's your name"

    ]:

        print(
            "Lily: I'm Lily, your personal AI assistant. ❤️"
        )

        continue



    if cleaned in [

        "what is my name",

        "whats my name",

        "what's my name",

        "who am i"

    ]:

        print(
            "Lily: Your name is Kiyoto."
        )

        continue



    # =========================================================
    # NATURAL LANGUAGE TOOL SELECTION
    # =========================================================

    tool_intent = understand_tool(user)

    if tool_intent:

        tool_name = tool_intent["tool"]

        tool_args = tool_intent["args"]


        # =====================================================
        # SCREENSHOT
        # =====================================================

        if tool_name == "take_screenshot":

            tool_result = tool_manager.run(
                tool_name,
                *tool_args
            )

            if not tool_result["success"]:

                print(
                    "Lily: The screenshot tool failed."
                )

                print(
                    "Reason:",
                    tool_result["message"]
                )

            else:

                result = tool_result["result"]

                if result.get("success"):

                    print(
                        "Lily: Screenshot saved here:"
                    )

                    print(
                        result["filename"]
                    )

                else:

                    print(
                        "Lily: I couldn't take the screenshot."
                    )

                    print(
                        "Error:",
                        result.get(
                            "error",
                            "Unknown error."
                        )
                    )

            continue


    # RUN TOOL SAFELY

    if tool_intent:
        tool_name = tool_intent.get("tool")
        tool_args = tool_intent.get("args", [])
        try:
            tool_result = tool_manager.run(tool_name, *tool_args)
        except Exception as e:
            print("Lily: The tool failed safely. ❤️")
            print("Reason:", e)
            continue

        if not isinstance(tool_result, dict) or not tool_result.get("success", False):
            print("Lily: The tool failed.")
            print("Reason:", tool_result.get("message", "Unknown error.") if isinstance(tool_result, dict) else tool_result)
            continue

        result = tool_result.get("result")

        if isinstance(result, dict) and result.get("confirmation_required"):
            if tool_name == "delete_path":
                pending_tool_confirmation = {"action": "delete", "path": result.get("path")}
                print(f"Lily: Are you sure you want to delete {result.get('path')}? Please answer yes or no. ⚠️")
                continue
            if tool_name == "restart_computer":
                pending_tool_confirmation = {"action": "restart"}
                print("Lily: Are you sure you want to restart your computer? Please answer yes or no. ⚠️")
                continue
            if tool_name == "shutdown_computer":
                pending_tool_confirmation = {"action": "shutdown"}
                print("Lily: Are you sure you want to shut down your computer? Please answer yes or no. ⚠️")
                continue

        if tool_name == "take_screenshot" and isinstance(result, dict):
            print("Lily: Screenshot saved here:" if result.get("success") else "Lily: I couldn't take the screenshot.")
            print(result.get("filename", result.get("error", "Unknown error.")))
        elif tool_name == "read_text_file" and isinstance(result, dict):
            print("Lily: Here's what's inside the file: 📖")
            print(result.get("content", "(The file is empty.)") if result.get("success") else result.get("error", "Unknown error."))
        elif tool_name == "list_files" and isinstance(result, dict):
            print("Lily: Files and folders:")
            for item in result.get("items", []):
                print("-", item.get("type","item"), ":", item.get("name","Unknown"))
        elif tool_name == "search_files" and isinstance(result, dict):
            results=result.get("results",[])
            print("Lily: I found:" if results else "Lily: I couldn't find that file. 🔎")
            for item in results:
                print("-",item)
        elif isinstance(result, dict):
            for k,v in result.items():
                print(f"{k}: {v}")
        elif isinstance(result,(list,tuple)):
            for item in result:
                print(item)
        else:
            print("Lily:", result)
        continue


# NORMAL INTENT ENGINE
# =========================================================
    # =========================================================
    # NORMAL INTENT ENGINE
    # =========================================================

    intent = understand(user)

    intent_type = intent["intent"]
    key = intent["key"]
    value = intent["value"]
    
    
    # =====================================================
    # SAVE PREFERENCE
    # =====================================================

    if intent_type == "SAVE_PREFERENCE":

        remember(
            memory,
            key,
            value
        )


        print(
            f"Lily: Got it! I'll remember your {key} as {value}. ❤️"
        )


        continue
    
    
    # =====================================================
    # GOALS
    # =====================================================

    if intent_type == "ADD_GOAL":

        add_goal(
            goals,
            value
        )

        save_goals(
            goals
        )


        print(
            f"Lily: I'll remember your goal: {value}. 🎯❤️"
        )

        continue



    if intent_type == "LIST_GOALS":

        if not goals:

            print(
                "Lily: You don't have any goals yet. 🎯"
            )

        else:

            print(
                "Lily: Your goals:"
            )

            for goal in goals:

                status = (
                    "completed"
                    if goal["completed"]
                    else "active"
                )

                print(
                    f"- {goal['task']} ({status})"
                )

        continue



    if intent_type == "COMPLETE_GOAL":

        success = complete_goal(
            goals,
        value
        )

        save_goals(
            goals
        )


        if success:
    
            print(
                f"Lily: Congratulations! I marked {value} as completed. 🎉"
            )

        else:

            print(
            f"Lily: I couldn't find that goal."
            )

        continue
    
    
    # =====================================================
    # LIST MEMORIES
    # =====================================================

    if intent_type == "LIST_MEMORIES":

        if not memory:

            print(
                "Lily: I don't remember anything yet. 🧠"
            )


        else:

            print(
                "Lily: I remember:"
            )


            for k, v in memory.items():

                category = v.get(
                    "category",
                    "general"
                )


                importance = v.get(
                    "importance",
                    "normal"
                )


                print(
                    f"- [{category}] {k}: {v['value']} "
                    f"(importance: {importance})"
                )


        continue


    # =====================================================
    # SHOW CATEGORY
    # =====================================================

    if intent_type == "SHOW_CATEGORY":

        if key == "preferences":
    
            category_memory = get_memories_by_category(
                memory,
                "preferences"
            )

            behavior_memory = get_memories_by_category(
                memory,
                "behavior"
            )

            category_memory.update(
                behavior_memory
            )

        else:

            category_memory = get_memories_by_category(
                memory,
                key
            )


        if not category_memory:

            print(
                f"Lily: I don't have any {key} memories yet."
            )


        else:

            print(
                f"Lily: Your {key} memories:"
            )


            for k, v in category_memory.items():

                print(
                    f"- {k}: {v['value']}"
                )


        continue
    
    
    # =====================================================
    # COUNT MEMORIES
    # =====================================================

    if intent_type == "COUNT_MEMORIES":

        print(
            f"Lily: I have {len(memory)} memories about you. 🧠"
        )

        continue



    # =====================================================
    # CLEAR ALL
    # =====================================================

    if intent_type == "CLEAR_ALL_MEMORIES":

        if memory:

            print(
                "Lily: Are you sure you want "
                "me to forget everything? "
                "Please answer yes or no."
            )

            waiting_clear_confirmation = True


        else:

            print(
                "Lily: I don't have any memories to delete."
            )


        continue


    # =====================================================
    # SAVE LIKE
    # =====================================================

    if intent_type == "SAVE_LIKE":

        remember(
            memory,
            key,
            value
        )


        set_context(
            key,
            value
        )


        print(
            f"Lily: Got it! I'll remember that you like {value}. ❤️"
        )


        continue
    
    
    # =====================================================
    # SAVE MEMORY
    # =====================================================

    if intent_type == "SAVE_MEMORY":
    
        remember(
            memory,
            key,
            value
        )

        set_state(
            state,
            "last_action",
            f"saved memory: {key}"
        )


        set_context(
            key,
            value
        )


        print(
            f"Lily: Got it! I'll remember "
            f"your {key} is {value}. ❤️"
        )

        continue



    # =====================================================
    # UPDATE MEMORY
    # =====================================================

    if intent_type == "UPDATE_MEMORY":

        old_memory = find_memory(
            memory,
            key
        )

        old = None

        if old_memory:
            old = old_memory["value"]


        remember(
            memory,
            key,
            value
        )


        set_state(
            state,
            "last_action",
            f"updated memory: {key}"
        )
        
        set_context(
            key,
            value
        )


        if old:

            print(
                f"Lily: Updated your {key} "
                f"from {old} to {value}. ❤️"
            )

        else:

            print(
                f"Lily: I saved your {key} as {value}. ❤️"
            )


        continue



    # =====================================================
    # READ MEMORY
    # =====================================================

    if intent_type == "READ_MEMORY":

        result = find_memory(
            memory,
            key
        )


        if result:
            
            set_context(
                key,
                result["value"]
            )

            pending_key = key

            pending_value = result["value"]

            waiting_memory_confirmation = True


            print(
                f"Lily: Your {key} is "
                f"{result['value']}, right?"
            )


        else:

            print(
                f"Lily: I don't have your {key} saved yet."
            )


        continue


    # =====================================================
    # CONTEXTUAL DISLIKE
    # =====================================================

    if intent_type == "CONTEXTUAL_DISLIKE":

        if has_context():

            context = get_context()

            context_key = context["key"]

            context_value = context["value"]


            if context_key.startswith("favorite "):

                category = context_key[
                    len("favorite "):
                ]

                dislike_key = (
                    "dislike " + category
                )

                remember(
                    memory,
                    dislike_key,
                    context_value
                )


                if context_key in memory:

                    del memory[context_key]

                    save_memory(
                        memory
                    )


                print(
                    f"Lily: Got it. I've noted "
                    f"that you don't like "
                    f"{context_value} anymore. ❤️"
                )


                clear_context()

            else:
    
                dislike_key = (
                    "dislike " + context_key
                )

                remember(
                    memory,
                    dislike_key,
                    context_value
                )

                clear_context()

                print(
                    f"Lily: Got it. I've noted "
                    f"that you don't like "
                    f"{context_value} anymore. ❤️"
                )

        else:

            print(
                "Lily: I understand you don't "
                "like something anymore, but "
                "I'm not sure what you mean."
            )
            
            
        continue
    
    # =====================================================
    # CONTEXTUAL USED TO LIKE
    # =====================================================

    if intent_type == "CONTEXTUAL_USED_TO_LIKE":

        if has_context():

            context = get_context()

            context_key = context["key"]

            context_value = context["value"]


            if context_key.startswith("favorite "):

                category = context_key[
                    len("favorite "):
                ]

                old_key = (
                    "used to like "
                    + category
                )

                remember(
                    memory,
                    old_key,
                    context_value
                )
                
                clear_context()


                print(
                    f"Lily: Got it. I'll remember "
                    f"that you used to like "
                    f"{context_value}. ❤️"
                )


            else:
    
                old_key = (
                    "used to like "
                    + context_key
                )

                remember(
                    memory,
                    old_key,
                    context_value
                )

                clear_context()

                print(
                    f"Lily: Got it. I'll remember "
                    f"that you used to like "
                    f"{context_value}. ❤️"
                )         


        else:

            print(
                "Lily: I understand you used "
                "to like something, but I don't "
                "know what you're referring to."
            )


        continue
    
    
    # =====================================================
    # DELETE MEMORY
    # =====================================================

    if intent_type == "DELETE_MEMORY":

        if forget_memory(
            memory,
            key
            ):
            
            set_state(
                state,
                "last_action",
                f"deleted memory: {key}"
            )

            print(
                f"Lily: I forgot your {key}. ❤️"
            )

        else:

            print(
                f"Lily: I don't have {key} saved."
            )


        continue


# =========================================================
# BACKUP
# =========================================================

    if lower == "backup":

        result = tool_manager.run(
            "backup"
        )

        if result["success"]:

            backup_folder, copied = result["result"]

            print(
                "Lily: Backup created successfully! 📦❤️"
            )

            print(
                "Location:",
                backup_folder
            )

            if copied:

                print(
                    "Files:",
                    ", ".join(copied)
                )

            else:

                print(
                    "Lily: There were no files to back up."
                )

        else:

            print(
                "Lily: I couldn't create the backup."
            )

            print(
                "Error:",
                result["message"]
            )

        continue
    
    
# =========================================================
# SHOW BACKUPS
# =========================================================

    if lower == "show backups":

        result = tool_manager.run(
            "list_backups"
        )

        if not result["success"]:

            print(
                "Lily: I couldn't get the backup list."
            )

            print(
                "Error:",
                result["message"]
            )

        else:

            backups = result["result"]

            if not backups:

                print(
                    "Lily: You don't have any backups yet. 📦"
                )

            else:

                print(
                    "Lily: Your backups:"
                )

                for backup in backups:

                    print(
                        "-",
                        backup
                    )

        continue
    
    
# =========================================================
# SYSTEM INFO
# =========================================================

    if lower == "system info":

        result = tool_manager.run(
            "system_info"
        )

        if result["success"]:

            info = result["result"]

            print(
                "Lily: Here's what I know about the computer:"
            )

            print(
                "System:",
                info["system"]
            )

            print(
                "Release:",
                info["release"]
            )

            print(
                "Machine:",
                info["machine"]
            )

            print(
                "Processor:",
                info["processor"]
            )

        else:

            print(
                "Lily: I couldn't get the system information."
            )

            print(
                "Error:",
                result["message"]
            )

        continue
    
    
# =========================================================
# CPU INFO
# =========================================================

    if tool_name == "cpu_info":
        
        print(
            "Lily: Here's your CPU information:"
        )

        if isinstance(result, dict):

            print(
                f"     CPU usage: {result.get('cpu_percent', 0)}%"
            )

            print(
                f"     CPU cores: {result.get('cpu_count', 0)}"
            )

        else:

            print(
                "     ",
                result
            )

        continue
    
    
# =========================================================
# MEMORY INFO
# =========================================================

    if lower == "memory info":

        result = tool_manager.run(
            "memory_info"
        )

        if result["success"]:

            info = result["result"]

            print(
                "Lily: RAM usage:",
                info["percent"],
                "%"
            )

            print(
                "Used:",
                info["used_gb"],
                "GB"
            )

            print(
                "Available:",
                info["available_gb"],
                "GB"
            )

        else:

            print(
                "Lily: I couldn't get the memory information."
            )

            print(
                "Error:",
                result["message"]
            )

        continue
    
    
# =========================================================
# DISK INFO
# =========================================================

    if lower == "disk info":

        result = tool_manager.run(
            "disk_info"
        )

        if result["success"]:

            info = result["result"]

            print(
                "Lily: Disk usage:",
                info["percent"],
                "%"
            )

            print(
                "Used:",
                info["used_gb"],
                "GB"
            )

            print(
                "Free:",
                info["free_gb"],
                "GB"
            )

        else:

            print(
                "Lily: I couldn't get the disk information."
            )

            print(
                "Error:",
                result["message"]
            )

        continue
    
    
    # =========================================================
    # SPEAK TEST
    # =========================================================

    if lower == "speak test":

        message = (
            "Hello Master. "
            "My voice system is working."
        )

        print(
            "Lily:",
            message
        )

        speak(
            message
        )

        continue
        
        
    # =========================================================
    # SHOW PLUGINS
    # =========================================================

    if lower == "show plugins":

        plugins = plugin_manager.list_plugins()

        if not plugins:

            print(
                "Lily: No plugins are loaded."
            )

        else:

            print(
                "Lily: Loaded plugins:"
            )

            for plugin in plugins:

                print(
                    "-",
                    plugin["name"],
                    ":",
                    plugin["description"]
                )

        continue
    
    
    # =========================================================
    # TEST PLUGIN
    # =========================================================

    if lower == "test plugin":

        result = plugin_manager.run(
            "hello_plugin"
        )

        if result["success"]:

            print(
                "Lily:",
                result["result"]
            )

        else:

            print(
                "Lily:",
                result["message"]
            )

        continue
    
    
# =========================================================
# BATTERY INFO
# =========================================================

    if tool_name == "battery_info":
        
        print(
            "Lily: Here's your battery information:"
        )

        if isinstance(result, dict):

            available = result.get(
                "available",
                False
            )

            percent = result.get(
                "percent",
                0
            )

            plugged = result.get(
                "plugged",
                False
            )

            if not available:

                print(
                    "     Battery information is not available."
                )

            else:

                print(
                    f"     Battery: {percent}%"
                )

                print(
                    "     Charging:",
                    "Yes" if plugged else "No"
                )

        else:

            print(
                "     ",
                result
            )

        continue
    
    
# =========================================================
# NETWORK INFO
# =========================================================

    if tool_name == "network_info":
        
        print(
            "Lily: Here's your network information:"
        )

        if isinstance(result, list):

            for network in result:

                name = network.get(
                    "name",
                    "Unknown network"
                )

                ipv4 = network.get(
                    "ipv4",
                    []
                )

                print()
                print(
                    f"     {name}"
                )

                if ipv4:

                    for address in ipv4:

                        print(
                            f"     IP address: {address}"
                        )

                else:

                    print(
                        "     IP address: None"
                    )

        else:

            print(
                "     ",
                result
            )

        continue
    
    
# =========================================================
# USER INFO
# =========================================================

    if lower == "user info":

        result = tool_manager.run(
            "user_info"
        )

        if result["success"]:

            info = result["result"]

            print(
                "Lily: Current user:",
                info["username"]
            )

            print(
                "Computer name:",
                info["computer_name"]
            )

        else:

            print(
                "Lily: I couldn't get user information."
            )

            print(
                "Error:",
                result["message"]
            )

        continue
    
    
# =========================================================
# DATE AND TIME
# =========================================================

    if tool_name == "datetime_info":
        
        if isinstance(result, dict):

            day = result.get(
                "day",
                "Unknown day"
            )

            date = result.get(
                "date",
                "Unknown date"
            )

            time = result.get(
                "time",
                "Unknown time"
            )

            print(
                f"Lily: It's {day}, {date}."
            )

            print(
                f"Lily: The current time is {time}."
            )

        else:

            print(
                "Lily:",
                result
            )

        continue
    
    
# =========================================================
# OPEN PROGRAM
# =========================================================

    if lower.startswith("open "):

        program = user[5:].strip()

        if not program:

            print(
                "Lily: What should I open?"
            )

            continue

        result = tool_manager.run(
            "launch_program",
            program
        )

        if result["success"]:

            print(
                "Lily: Opening",
                program,
                "🚀"
            )

        else:

            info = result["result"]

            if not info["success"]:

                print(
                    "Lily: I couldn't open that."
                )

                print(
                    "Error:",
                    info["error"]
                )

        continue
    
# =========================================================
# LIST FILES
# =========================================================

    if lower.startswith("list files"):

        folder = user[len("list files"):].strip()

        if not folder:

            folder = os.getcwd()

        tool_result = tool_manager.run(
            "list_files",
            folder
        )

        if not tool_result["success"]:

            print(
                "Lily: The file tool failed."
            )

            print(
                "Reason:",
                tool_result["message"]
            )

        else:

            result = tool_result["result"]

            if not result["success"]:

                print(
                    "Lily: I couldn't list that folder."
                )

                print(
                    "Reason:",
                    result["message"]
                )

            else:

                print(
                    "Lily: Contents of:",
                    result["folder"]
                )

                items = result["items"]

                if not items:

                    print(
                        "Lily: The folder is empty."
                    )

                else:

                    for item in items:

                        print(
                            "-",
                            item["type"],
                            ":",
                            item["name"]
                        )

        continue
    
    
# =========================================================
# SEARCH FILES
# =========================================================

    if lower.startswith("search files"):

        search_text = user[len("search files"):].strip()

        parts = search_text.rsplit(" ", 1)

        if len(parts) != 2:

            print(
                "Lily: Use: search files <folder> <filename>"
            )

            continue

        folder = parts[0]
        filename = parts[1]

        tool_result = tool_manager.run(
            "search_files",
            folder,
            filename
        )

        if not tool_result["success"]:

            print(
                "Lily: The file tool failed."
            )

            print(
                "Reason:",
                tool_result["message"]
            )

        else:

            result = tool_result["result"]

            if not result["success"]:

                print(
                    "Lily: I couldn't search that folder."
                )

                print(
                    "Reason:",
                    result["message"]
                )

            else:

                results = result["results"]

                if not results:

                    print(
                        "Lily: I couldn't find that file."
                    )

                else:

                    print(
                        "Lily: I found:"
                    )

                    for path in results:

                        print(
                            "-",
                            path
                        )

        continue
    
    
# =========================================================
# SCREENSHOT
# =========================================================

    if lower == "take screenshot":

        screenshot_folder = os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ),
            "screenshots"
        )

        os.makedirs(
            screenshot_folder,
            exist_ok=True
        )

        filename = os.path.join(
            screenshot_folder,
            "screenshot_" +
            datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            ) +
            ".png"
        )

        result = tool_manager.run(
            "take_screenshot",
            filename
        )

        if result["success"]:

            info = result["result"]

            if info["success"]:

                print(
                    "Lily: Screenshot saved! 📸"
                )

                print(
                    "Location:",
                    info["filename"]
                )

            else:

                print(
                    "Lily: I couldn't take the screenshot."
                )

                print(
                    "Error:",
                    info["error"]
                )

        else:

            print(
                "Lily: The screenshot tool failed."
            )

            print(
                "Error:",
                result["message"]
            )

        continue
    
                  
    # =========================================================
    # NORMAL AI CHAT
    # =========================================================

    brain_result = think(
        user,
        learning
    )

    response_mode = brain_result.get(
        "response_mode",
        "normal"
    )
    
    difficulty = brain_result.get(
        "difficulty",
        "normal"
    )

    answer_length = brain_result.get(
        "answer_length",
        "normal"
    )

    technical_terms = brain_result.get(
        "technical_terms",
        "normal"
    )


    # =========================================================
    # BUILD RESPONSE INSTRUCTIONS
    # =========================================================

    response_instructions = ""


    # ---------------------------------------------------------
    # RESPONSE MODE
    # ---------------------------------------------------------

    if response_mode == "simple":

        response_instructions += """
    RESPONSE MODE: SIMPLE

    Answer the user in simple everyday English.

    Rules:
    - Explain the main idea first.
    - Use short and clear sentences.
    - Explain one idea at a time.
    - Do not assume the user already knows the subject.
    """


    elif response_mode == "detailed":

        response_instructions += """
    RESPONSE MODE: DETAILED

    Give the user a detailed explanation.

    Rules:
    - Explain the main idea clearly.
    - Break complicated ideas into sections.
    - Explain important concepts.
    - Give examples when useful.
    """


    # ---------------------------------------------------------
    # DIFFICULTY
    # ---------------------------------------------------------

    if difficulty == "beginner":

        response_instructions += """
    DIFFICULTY: BEGINNER

    The user is a beginner.

    Rules:
    - Start from the basics.
    - Do not assume prior knowledge.
    - Use familiar real-world examples.
    - If a technical word is necessary, explain it immediately.
    """


    # ---------------------------------------------------------
    # ANSWER LENGTH
    # ---------------------------------------------------------

    if answer_length == "short":

        response_instructions += """
    ANSWER LENGTH: SHORT

    Keep the answer concise.

    Rules:
    - Focus only on the most important information.
    - Avoid unnecessary background information.
    - Prefer a few clear paragraphs instead of a long lecture.
    """


    elif answer_length == "long":

        response_instructions += """
    ANSWER LENGTH: LONG

    Give enough explanation to fully understand the subject.

    Rules:
    - Cover the important parts.
    - Use examples when useful.
    - Organize the answer clearly.
    """


    # ---------------------------------------------------------
    # TECHNICAL TERMS
    # ---------------------------------------------------------

    if technical_terms == "low":

        response_instructions += """
    TECHNICAL TERMS: LOW

    Avoid unnecessary technical terminology.

    If an important technical word must be used:
    1. Say the word.
    2. Immediately explain what it means in simple language.
    3. Continue using simple language afterward.
    """


    elif technical_terms == "normal":

        response_instructions += """
    TECHNICAL TERMS: NORMAL

    Use technical terms when they are useful.

    Explain important technical terms clearly.
    """


    # =========================================================
    # FINAL RESPONSE RULES
    # =========================================================

    response_instructions += """

    IMPORTANT:

    - Answer the user's actual question.
    - Do not talk about these instructions.
    - Do not mention response modes or response plans.
    - Do not repeat the user's question unnecessarily.
    - Do not invent facts.
    - If you are unsure about something, say so.
    """


    # =========================================================
    # BUILD AI PROMPT
    # =========================================================

    prompt = (

        build_system_prompt()

        + response_instructions

        + conversation

        + f"<|im_start|>user\n{user}\n<|im_end|>\n"

        + "<|im_start|>assistant\n"

    )


    # =========================================================
    # RUN AI ENGINE
    # =========================================================

    try:

        result = subprocess.run(

            [

                LLAMA,

                "-m", MODEL,

                "-c", "2048",

                "-n", "128",

                "--no-display-prompt",

                "-p", prompt

            ],

            capture_output=True,

            text=True,

            timeout=120

        )


    except Exception as e:

        print(
            "Lily: I couldn't start my AI engine.",
            e
        )

        continue


    if result.returncode != 0:

        print(
            "Lily: My AI engine returned an error."
        )

        continue


    # =========================================================
    # CLEAN AI RESPONSE
    # =========================================================

    answer = result.stdout.strip()

    answer = answer.encode(
        "utf-8",
        errors="ignore"
    ).decode(
        "utf-8",
        errors="ignore"
    )


    if not answer:

        answer = "Sorry, I couldn't think of an answer."


    if "<|im_end|>" in answer:

        answer = answer.split(
            "<|im_end|>"
        )[0].strip()


    if "<|im_start|>" in answer:

        answer = answer.split(
            "<|im_start|>"
        )[0].strip()


    # =========================================================
    # DISPLAY RESPONSE
    # =========================================================

    print(
        "Lily:",
        answer
    )


    # =========================================================
    # SAVE CONVERSATION
    # =========================================================

    conversation += (

        f"<|im_start|>user\n"

        f"{user}\n"

        f"<|im_end|>\n"

        f"<|im_start|>assistant\n"

        f"{answer}\n"

        f"<|im_end|>\n"

    )


    # =========================================================
    # KEEP CONVERSATION MEMORY SMALL
    # =========================================================

    conversation = "\n".join(
        conversation.split("\n")[-300:]
    )