from Libs.GuiLib.gui_majors import *


class ExpenseSummaryFrame(ContentFrame):
    def __init__(self, root):
        super().__init__(root, "Expense Summary")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)

        # TITLE
        self._title = TitleLabel(self, text="Account Expense Map")
        self._title.grid(row=0, column=0, **TitleLabel.grid_args)

        lbl_kwargs = {
            'anchor': W,
        }

        display_kwargs = {
            'anchor': E,
        }

        # ACTION FRAME
        self._action_frame = StandardFrame(self)
        self._action_frame.grid(row=1, column=0, **StandardFrame.grid_args)
        self._action_frame.grid_columnconfigure(0, weight=1)
        self._action_frame.grid_columnconfigure(1, weight=1)

        # TOTAL EXPENSES
        self._total_expenses_lbl = StandardLabel(self._action_frame, text="Total Expenses", **lbl_kwargs)
        self._total_expenses_lbl.grid(row=0, column=0, **StandardLabel.grid_args)

        self._total_expenses_display = StandardLabel(self._action_frame, "")
        self._total_expenses_display.grid(row=0, column=1, **StandardLabel.grid_args)

        # TOTAL YEARLY
        self._total_yearly_lbl = StandardLabel(self._action_frame, text="Total Yearly", **lbl_kwargs)
        self._total_yearly_lbl.grid(row=1, column=0, **StandardLabel.grid_args)

        self._total_yearly_display = StandardLabel(self._action_frame, "", **display_kwargs)
        self._total_yearly_display.grid(row=1, column=1, **StandardLabel.grid_args)

        # TOTAL MONTHLY
        self._total_monthly_lbl = StandardLabel(self._action_frame, text="Total Monthly", **lbl_kwargs)
        self._total_monthly_lbl.grid(row=2, column=0, **StandardLabel.grid_args)

        self._total_monthly_display = StandardLabel(self._action_frame, "", **display_kwargs)
        self._total_monthly_display.grid(row=2, column=1, **StandardLabel.grid_args)

        # TOTAL SEMI MONTHLY
        self._total_semi_monthly_lbl = StandardLabel(self._action_frame, text="Total Semi-Monthly", **lbl_kwargs)
        self._total_semi_monthly_lbl.grid(row=3, column=0, **StandardLabel.grid_args)

        self._total_semi_monthly_display = StandardLabel(self._action_frame, "", **display_kwargs)
        self._total_semi_monthly_display.grid(row=3, column=1, **StandardLabel.grid_args)

    def update_expense_summary(self, expenses_list):
        # TOTAL EXPENSES
        expense_count = len(expenses_list)
        self._total_expenses_display['text'] = "{}".format(expense_count)

        # YEARLY
        total_yearly = 0
        for expense in expenses_list:
            expense_yearly = expense.get_yearly_value()
            total_yearly += expense_yearly
        self._total_yearly_display['text'] = "{:.2f}".format(total_yearly)

        # MONTHLY
        total_monthly = total_yearly / 12
        self._total_monthly_display['text'] = "{:.2f}".format(total_monthly)

        # SEMI MONTHLY
        total_semi_monthly = total_monthly / 2
        self._total_semi_monthly_display['text'] = "{:.2f}".format(total_semi_monthly)