from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Callback-data convention: values are separated with ":" (never "|").


def main_menu_kb():
    kb = [
        [
            InlineKeyboardButton("🔑 Manage Account", callback_data="manage_account"),
            InlineKeyboardButton("🛡️ Safe / Guard", callback_data="guard_account"),
        ],
        [InlineKeyboardButton("👤 My Accounts", callback_data="my_accounts")],
    ]
    return InlineKeyboardMarkup(kb)


def admin_back_kb():
    kb = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")]]
    return InlineKeyboardMarkup(kb)


# ── Manage dashboard (after sending hex) ─────────────────────────────────────
def manage_dashboard_kb(guard_active: bool = False):
    guard_label = "🛡️ Guard: ON" if guard_active else "🛡️ Safe Guard: OFF"
    kb = [
        [
            InlineKeyboardButton("📱 Device Dashboard", callback_data="mng_devices"),
            InlineKeyboardButton("🗑️ Clear All", callback_data="mng_clear_all"),
        ],
        [
            InlineKeyboardButton("📨 Fetch OTP", callback_data="mng_fetch_otp"),
            InlineKeyboardButton("📧 Change Mail", callback_data="mng_change_mail"),
        ],
        [
            InlineKeyboardButton("🧪 Check Mail", callback_data="mail_check"),
            InlineKeyboardButton("🔐 2FA", callback_data="mng_2fa"),
        ],
        [
            InlineKeyboardButton("📤 Export Hex", callback_data="mng_export_hex"),
            InlineKeyboardButton(guard_label, callback_data="mng_guard_toggle"),
        ],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(kb)


def device_dashboard_kb(devices: list, guard_active: bool = False):
    """One button per device + guard toggle + revoke-all + revoke-bot + back."""
    kb = []
    for i, dev in enumerate(devices):
        model = (dev.get("device_model") or "Unknown")[:18]
        platform = (dev.get("platform") or "")[:12]
        cur = " 🤖 BOT" if dev.get("current") else ""
        label = f"📱 {i + 1}. {model} · {platform}{cur}"
        kb.append([InlineKeyboardButton(label, callback_data=f"dev:{i}")])

    kb.append([
        InlineKeyboardButton("🔌 Terminate All Other Sessions", callback_data="revoke_all"),
    ])
    guard_label = "🛡️ Guard: ON" if guard_active else "🛡️ Guard: OFF"
    kb.append([
        InlineKeyboardButton(guard_label, callback_data="guard_toggle"),
    ])
    kb.append([
        InlineKeyboardButton("🔴 Revoke Bot Connection", callback_data="revoke_bot"),
    ])
    kb.append([
        InlineKeyboardButton("🔙 Back to Dashboard", callback_data="mng_back_dash"),
    ])
    return InlineKeyboardMarkup(kb)


def terminate_confirm_kb(device_idx: int):
    kb = [
        [
            InlineKeyboardButton("✅ Yes, Terminate", callback_data=f"dev_yes:{device_idx}"),
            InlineKeyboardButton("❌ Cancel", callback_data="dev_no"),
        ]
    ]
    return InlineKeyboardMarkup(kb)


def revoke_bot_confirm_kb():
    kb = [
        [
            InlineKeyboardButton("🔴 Yes, Revoke & Remove", callback_data="revoke_bot_yes"),
            InlineKeyboardButton("❌ Cancel", callback_data="dev_no"),
        ]
    ]
    return InlineKeyboardMarkup(kb)


def clear_all_confirm_kb():
    kb = [
        [
            InlineKeyboardButton("✅ Yes, Clear Everything", callback_data="clr_yes"),
            InlineKeyboardButton("❌ Cancel", callback_data="clr_no"),
        ]
    ]
    return InlineKeyboardMarkup(kb)


def otp_menu_kb():
    kb = [
        [InlineKeyboardButton("📨 Read Latest OTP", callback_data="otp_read")],
        [InlineKeyboardButton("🔙 Back to Dashboard", callback_data="mng_back_dash")],
    ]
    return InlineKeyboardMarkup(kb)


def back_to_dashboard_kb():
    kb = [[InlineKeyboardButton("🔙 Back to Dashboard", callback_data="mng_back_dash")]]
    return InlineKeyboardMarkup(kb)


def cancel_kb(action: str):
    kb = [[InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{action}")]]
    return InlineKeyboardMarkup(kb)


def change_mail_confirm_kb():
    kb = [
        [InlineKeyboardButton("✅ Yes, Change Mail", callback_data="cm_yes")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cm_no")],
    ]
    return InlineKeyboardMarkup(kb)


def twofa_menu_kb():
    """2FA management menu."""
    kb = [
        [InlineKeyboardButton("🔐 Set / Change 2FA Password", callback_data="2fa_set")],
        [InlineKeyboardButton("🗑️ Remove 2FA Password", callback_data="2fa_remove")],
        [InlineKeyboardButton("ℹ️ Check 2FA Status", callback_data="2fa_status")],
        [InlineKeyboardButton("🔙 Back", callback_data="mng_back_dash")],
    ]
    return InlineKeyboardMarkup(kb)


# ── My Accounts ──────────────────────────────────────────────────────────────
def accounts_pagination_kb(accounts: list, page: int, total_pages: int):
    kb = []
    start = page * 5
    end = min(start + 5, len(accounts))

    for i in range(start, end):
        acc = accounts[i]
        label = f"📱 {acc.get('name', 'Unknown')} ({acc.get('phone', 'Unknown')})"
        kb.append([InlineKeyboardButton(label, callback_data=f"acc_view:{acc['_id']}")])

    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("◀️ Prev", callback_data=f"acc_page:{page - 1}"))
    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton("Next ▶️", callback_data=f"acc_page:{page + 1}"))
    if nav_row:
        kb.append(nav_row)

    kb.append([InlineKeyboardButton("🔄 Refresh", callback_data="acc_refresh")])
    kb.append([InlineKeyboardButton("🔙 Main Menu", callback_data="back_main")])
    return InlineKeyboardMarkup(kb)


def account_detail_kb(account_id: str, guard_active: bool = False):
    guard_label = "🛡️ Guard: ON" if guard_active else "🛡️ Guard: OFF"
    kb = [
        [
            InlineKeyboardButton("📨 Fetch OTP", callback_data=f"acc_otp:{account_id}"),
            InlineKeyboardButton("🔌 Revoke Bot", callback_data=f"acc_revoke:{account_id}"),
        ],
        [
            InlineKeyboardButton("🔓 Allow Login (60s)", callback_data=f"acc_allow:{account_id}"),
        ],
        [InlineKeyboardButton(guard_label, callback_data=f"acc_guard:{account_id}")],
        [InlineKeyboardButton("⚙️ Full Operations", callback_data=f"acc_fullops:{account_id}")],
        [InlineKeyboardButton("🔙 Back to Accounts", callback_data="acc_back")],
    ]
    return InlineKeyboardMarkup(kb)


def full_operations_kb(account_id: str, guard_active: bool = False):
    """Full operations menu for a saved account (My Accounts → Full Operations)."""
    guard_label = "🛡️ Guard: ON" if guard_active else "🛡️ Safe Guard: OFF"
    kb = [
        [
            InlineKeyboardButton("📱 Device Dashboard", callback_data=f"fo_devices:{account_id}"),
            InlineKeyboardButton("🗑️ Clear All", callback_data=f"fo_clear:{account_id}"),
        ],
        [
            InlineKeyboardButton("📨 Fetch OTP", callback_data=f"fo_otp:{account_id}"),
            InlineKeyboardButton("📧 Change Mail", callback_data=f"fo_changemail:{account_id}"),
        ],
        [
            InlineKeyboardButton("🧪 Check Mail", callback_data=f"fo_checkmail:{account_id}"),
            InlineKeyboardButton("🔐 2FA", callback_data=f"fo_2fa:{account_id}"),
        ],
        [
            InlineKeyboardButton("📤 Export Hex", callback_data=f"fo_export:{account_id}"),
            InlineKeyboardButton(guard_label, callback_data=f"fo_guard:{account_id}"),
        ],
        [InlineKeyboardButton("🔙 Back to Account", callback_data=f"acc_view:{account_id}")],
    ]
    return InlineKeyboardMarkup(kb)


def fo_back_kb(account_id: str):
    """Back button that returns to Full Operations menu."""
    kb = [[InlineKeyboardButton("🔙 Back to Full Ops", callback_data=f"acc_fullops:{account_id}")]]
    return InlineKeyboardMarkup(kb)



def fo_device_dashboard_kb(account_id: str, devices: list, guard_active: bool = False):
    """Full Ops device list — terminate, revoke all, revoke bot."""
    kb = []
    for i, dev in enumerate(devices):
        model = (dev.get("device_model") or "Unknown")[:18]
        platform = (dev.get("platform") or "")[:12]
        cur = " 🤖 BOT" if dev.get("current") else ""
        label = f"📱 {i + 1}. {model} · {platform}{cur}"
        kb.append([InlineKeyboardButton(label, callback_data=f"fo_dev:{account_id}:{i}")])

    kb.append([
        InlineKeyboardButton("🔌 Terminate All Other", callback_data=f"fo_revoke_all:{account_id}"),
    ])
    guard_label = "🛡️ Guard: ON" if guard_active else "🛡️ Guard: OFF"
    kb.append([
        InlineKeyboardButton(guard_label, callback_data=f"fo_guard:{account_id}"),
    ])
    kb.append([
        InlineKeyboardButton("🔴 Revoke Bot Connection", callback_data=f"fo_revoke_bot:{account_id}"),
    ])
    kb.append([
        InlineKeyboardButton("🔙 Back to Full Ops", callback_data=f"acc_fullops:{account_id}"),
    ])
    return InlineKeyboardMarkup(kb)


def fo_terminate_confirm_kb(account_id: str, device_idx: int):
    kb = [
        [
            InlineKeyboardButton("✅ Yes, Terminate", callback_data=f"fo_dev_yes:{account_id}:{device_idx}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"fo_devices:{account_id}"),
        ]
    ]
    return InlineKeyboardMarkup(kb)


def fo_revoke_bot_confirm_kb(account_id: str):
    kb = [
        [
            InlineKeyboardButton("🔴 Yes, Revoke & Remove", callback_data=f"fo_revoke_bot_yes:{account_id}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"fo_devices:{account_id}"),
        ]
    ]
    return InlineKeyboardMarkup(kb)


def fo_clear_confirm_kb(account_id: str):
    kb = [
        [
            InlineKeyboardButton("✅ Yes, Clear Everything", callback_data=f"fo_clear_yes:{account_id}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"acc_fullops:{account_id}"),
        ]
    ]
    return InlineKeyboardMarkup(kb)

def fo_twofa_kb(account_id: str):
    kb = [
        [InlineKeyboardButton("🔐 Set / Change 2FA", callback_data=f"fo_2fa_set:{account_id}")],
        [InlineKeyboardButton("🗑️ Remove 2FA", callback_data=f"fo_2fa_remove:{account_id}")],
        [InlineKeyboardButton("ℹ️ Check 2FA Status", callback_data=f"fo_2fa_status:{account_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data=f"acc_fullops:{account_id}")],
    ]
    return InlineKeyboardMarkup(kb)


# ── Guard ────────────────────────────────────────────────────────────────────
def guard_back_kb():
    kb = [
        [InlineKeyboardButton("🛡️ Guard Status", callback_data="guard_status")],
        [InlineKeyboardButton("🛑 Deactivate Guard", callback_data="guard_deactivate")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(kb)


# ── Owner Access (control other users) ───────────────────────────────────────
def owner_access_accounts_kb(accounts: list, target_user_id: int, page: int = 0):
    """Owner viewing another user's accounts."""
    kb = []
    start = page * 5
    end = min(start + 5, len(accounts))
    for i in range(start, end):
        acc = accounts[i]
        label = f"📱 {acc.get('name', 'Unknown')} ({acc.get('phone', 'Unknown')})"
        kb.append([InlineKeyboardButton(
            label, callback_data=f"oa_view:{target_user_id}:{acc['_id']}"
        )])
    kb.append([InlineKeyboardButton("🔙 Cancel Access", callback_data="back_main")])
    return InlineKeyboardMarkup(kb)


def owner_full_ops_kb(target_user_id: int, account_id: str, guard_active: bool = False):
    """Full ops when owner is controlling another user's account."""
    guard_label = "🛡️ Guard: ON" if guard_active else "🛡️ Safe Guard: OFF"
    prefix = f"oafo:{target_user_id}:{account_id}"
    kb = [
        [
            InlineKeyboardButton("📱 Device Dashboard", callback_data=f"{prefix}:devices"),
            InlineKeyboardButton("🗑️ Clear All", callback_data=f"{prefix}:clear"),
        ],
        [
            InlineKeyboardButton("📨 Fetch OTP", callback_data=f"{prefix}:otp"),
            InlineKeyboardButton("📤 Export Hex", callback_data=f"{prefix}:export"),
        ],
        [
            InlineKeyboardButton(guard_label, callback_data=f"{prefix}:guard"),
        ],
        [InlineKeyboardButton("🔙 Back", callback_data=f"oa_view:{target_user_id}:{account_id}")],
    ]
    return InlineKeyboardMarkup(kb)
