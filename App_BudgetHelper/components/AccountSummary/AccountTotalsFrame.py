from Libs.GuiLib.gui_standards import *


class AccountTotalsFrame(StandardFrame):
    def __init__(self, root):
        super().__init__(root)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # TOTALS TITLE
        self._totals_lbl_title = TitleLabel(self, text="Totals")
        self._totals_lbl_title.grid(row=0, column=0, columnspan=2, **TitleLabel.grid_args)

        lbl_kwargs = {
            'anchor': W,
        }

        display_kwargs = {
            'anchor': E,
        }

        # YEARLY
        self._total_yearly_lbl = StandardLabel(self, text="Yearly", **lbl_kwargs)
        self._total_yearly_lbl.grid(row=1, column=0, **StandardLabel.grid_args)

        self._total_yearly_display = StandardLabel(self, "", **display_kwargs)
        self._total_yearly_display.grid(row=1, column=1, **StandardLabel.grid_args)

        # MONTHLY
        self._total_monthly_lbl = StandardLabel(self, text="Monthly", **lbl_kwargs)
        self._total_monthly_lbl.grid(row=2, column=0, **StandardLabel.grid_args)

        self._total_monthly_display = StandardLabel(self, "", **display_kwargs)
        self._total_monthly_display.grid(row=2, column=1, **StandardLabel.grid_args)

        # SEMI MONTHLY
        self._total_semi_monthly_lbl = StandardLabel(self, text="Semi-Monthly", **lbl_kwargs)
        self._total_semi_monthly_lbl.grid(row=3, column=0, **StandardLabel.grid_args)

        self._total_semi_monthly_display = StandardLabel(self, "", **display_kwargs)
        self._total_semi_monthly_display.grid(row=3, column=1, **StandardLabel.grid_args)

    def clear_displays(self):
        for display in [
            self._total_yearly_display,
            self._total_monthly_display,
            self._total_semi_monthly_display,
        ]:
            display['text'] = ""

    def show_account_stats(self, expenses_list):
        # SHOW TOTALS
        total_yearly = 0
        for expense in expenses_list:
            yearly_value = expense.get_yearly_value()
            total_yearly += float(yearly_value)
        self._total_yearly_display['text'] = "{:.2f}".format(total_yearly)

        total_monthly = total_yearly / 12
        self._total_monthly_display['text'] = "{:.2f}".format(total_monthly)

        total_semi_monthly = total_monthly / 2
        self._total_semi_monthly_display['text'] = "{:.2f}".format(total_semi_monthly)


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)

    frame = AccountTotalsFrame(root)
    frame.grid(row=0, column=0, sticky=grid_style.sticky.all)

    root.mainloop()
