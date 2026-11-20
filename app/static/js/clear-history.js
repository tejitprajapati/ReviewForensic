document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("clearHistoryBtn");
    if (!button) return;

    const overlay = document.createElement("div");
    overlay.id = "cyberpulseConfirm";

    overlay.innerHTML = `
      <div class="cp-dialog" role="dialog"
           aria-modal="true"
           aria-labelledby="cpTitle"
           aria-describedby="cpDescription">
        <div class="cp-heading">
          <span class="cp-shield">⚠</span>
          <div>
            <strong>REVIEWFORENSIC SECURITY</strong>
            <small>Critical action confirmation</small>
          </div>
        </div>
        <h2 id="cpTitle">Clear all review history?</h2>
        <p id="cpDescription">
          This will permanently delete all saved reviews.
          This action cannot be undone from the dashboard.
        </p>
        <div class="cp-actions">
          <button type="button" id="cpCancel">Cancel</button>
          <button type="button" id="cpDelete">
            Delete History
          </button>
        </div>
      </div>
    `;

    const style = document.createElement("style");
    style.textContent = `
      #cyberpulseConfirm {
        display: none;
        position: fixed;
        inset: 0;
        background: rgba(2, 6, 23, .82);
        backdrop-filter: blur(6px);
        z-index: 99999;
        align-items: center;
        justify-content: center;
        padding: 20px;
      }
      #cyberpulseConfirm .cp-dialog {
        background: #152139;
        border: 1px solid #344968;
        border-radius: 18px;
        padding: 28px;
        width: min(100%, 440px);
        color: #eaf2ff;
        box-shadow: 0 24px 70px rgba(0,0,0,.5);
      }
      #cyberpulseConfirm .cp-heading {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 24px;
      }
      #cyberpulseConfirm .cp-heading strong {
        display: block;
        color: #38bdf8;
        letter-spacing: 1px;
        font-size: 13px;
      }
      #cyberpulseConfirm .cp-heading small {
        display: block;
        color: #94a3b8;
        margin-top: 5px;
      }
      #cyberpulseConfirm .cp-shield {
        background: #402331;
        color: #fb7185;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 24px;
      }
      #cyberpulseConfirm h2 {
        font-size: 21px;
        margin: 0 0 14px;
      }
      #cyberpulseConfirm p {
        color: #aabbd4;
        font-size: 14px;
        line-height: 1.7;
      }
      #cyberpulseConfirm .cp-actions {
        display: flex;
        justify-content: flex-end;
        gap: 12px;
        margin-top: 28px;
      }
      #cyberpulseConfirm button {
        border: none;
        border-radius: 9px;
        padding: 12px 18px;
        font-weight: 600;
        cursor: pointer;
      }
      #cpCancel {
        background: #29354c;
        color: white;
      }
      #cpDelete {
        background: #e04f65;
        color: white;
      }
      #cyberpulseConfirm button:focus-visible {
        outline: 2px solid #38bdf8;
        outline-offset: 3px;
      }
    `;

    document.head.appendChild(style);
    document.body.appendChild(overlay);

    const cancel = overlay.querySelector("#cpCancel");
    const remove = overlay.querySelector("#cpDelete");

    function closeDialog() {
        overlay.style.display = "none";
        button.focus();
    }

    button.addEventListener("click", () => {
        overlay.style.display = "flex";
        cancel.focus();
    });

    cancel.addEventListener("click", closeDialog);

    overlay.addEventListener("click", (event) => {
        if (event.target === overlay) closeDialog();
    });

    overlay.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeDialog();
        }
        if (event.key === "Tab") {
            event.preventDefault();
            if (document.activeElement === cancel) {
                remove.focus();
            } else {
                cancel.focus();
            }
        }
    });

    remove.addEventListener("click", () => {
        remove.disabled = true;
        remove.textContent = "Deleting...";

        const form = document.createElement("form");
        form.method = "POST";
        form.action = "/history/clear";
        document.body.appendChild(form);
        form.submit();
    });
});
