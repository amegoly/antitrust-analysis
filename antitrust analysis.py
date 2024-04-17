import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import ttkbootstrap as ttk
import openai

class MergerAnalysisTool:
    def __init__(self, master, api_key):
        self.master = master
        master.title("Merger Analysis Tool")
        self.api_key = api_key

        self.industries = ["Technology", "Healthcare", "Finance", "Energy", "Consumer Goods", "Manufacturing", "Telecommunications", "Media", "Retail", "Automotive"]
        self.countries = ["USA", "EU", "China", "UK", "Germany", "France", "Japan", "Canada", "Australia", "Brazil", "India", "Russia", "South Korea", "Mexico", "Indonesia"]
        self.overlap_options = ["No Overlap", "Low Overlap", "Moderate Overlap", "High Overlap"]

        self.bidder = tk.StringVar()
        self.target = tk.StringVar()
        self.bidder_industry = tk.StringVar(value=self.industries[0])
        self.target_industry = tk.StringVar(value=self.industries[0])
        self.bidder_market_share = tk.StringVar()
        self.target_market_share = tk.StringVar()
        self.product_overlap = tk.StringVar(value=self.overlap_options[0])

        ttk.Label(master, text="Bidder:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master, textvariable=self.bidder).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(master, text="Target:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master, textvariable=self.target).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(master, text="Bidder Industry:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Combobox(master, textvariable=self.bidder_industry, values=self.industries).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(master, text="Target Industry:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Combobox(master, textvariable=self.target_industry, values=self.industries).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(master, text="Bidder Countries:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.bidder_countries_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, exportselection=False)
        for country in self.countries:
            self.bidder_countries_listbox.insert(tk.END, country)
        self.bidder_countries_listbox.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(master, text="Target Countries:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.target_countries_listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, exportselection=False)
        for country in self.countries:
            self.target_countries_listbox.insert(tk.END, country)
        self.target_countries_listbox.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(master, text="Bidder Market Share:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master, textvariable=self.bidder_market_share).grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(master, text="Target Market Share:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(master, textvariable=self.target_market_share).grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(master, text="Product Overlap:").grid(row=8, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Combobox(master, textvariable=self.product_overlap, values=self.overlap_options).grid(row=8, column=1, padx=5, pady=5)

        analyze_button = ttk.Button(master, text="Analyze", command=self.analyze_merger, bootstyle="success")
        analyze_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        self.result_text = tk.Text(master, wrap=tk.WORD, width=60, height=20)
        self.result_text.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

    def analyze_merger(self):
        bidder = self.bidder.get()
        target = self.target.get()
        bidder_industry = self.bidder_industry.get()
        target_industry = self.target_industry.get()
        bidder_countries = [self.bidder_countries_listbox.get(idx) for idx in self.bidder_countries_listbox.curselection()]
        target_countries = [self.target_countries_listbox.get(idx) for idx in self.target_countries_listbox.curselection()]
        bidder_market_share = float(self.bidder_market_share.get())
        target_market_share = float(self.target_market_share.get())
        product_overlap = self.product_overlap.get()

        regulators = self.identify_regulators(bidder_countries, target_countries)
        timelines = self.get_approval_timelines(regulators)
        probability = self.calculate_approval_probability(bidder_market_share, target_market_share, product_overlap)

        analysis_text = f"Merger Analysis Results:\n\n"
        analysis_text += f"Bidder: {bidder}\n"
        analysis_text += f"Target: {target}\n"
        analysis_text += f"Bidder Industry: {bidder_industry}\n"
        analysis_text += f"Target Industry: {target_industry}\n"
        analysis_text += f"Bidder Countries: {', '.join(bidder_countries)}\n"
        analysis_text += f"Target Countries: {', '.join(target_countries)}\n"
        analysis_text += f"Bidder Market Share: {bidder_market_share:.2%}\n"
        analysis_text += f"Target Market Share: {target_market_share:.2%}\n"
        analysis_text += f"Product Overlap: {product_overlap}\n\n"

        analysis_text += f"Regulators Involved:\n"
        for regulator in regulators:
            analysis_text += f"- {regulator}\n"

        analysis_text += f"\nApproval Timelines:\n"
        for regulator, timeline in timelines.items():
            analysis_text += f"{regulator}: {timeline} months\n"

        analysis_text += f"\nProbability of Approval: {probability:.2%}\n\n"

        for regulator in regulators:
            analysis_text += self.analyze_regulator(regulator, bidder, target, bidder_market_share, target_market_share, product_overlap)

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, analysis_text)

    def analyze_regulator(self, regulator, bidder, target, bidder_market_share, target_market_share, product_overlap):
        openai.api_key = self.api_key

        prompt = f"Analyze the potential antitrust concerns for the merger between {bidder} and {target} from the perspective of {regulator}. Consider the following factors:\n\n"
        prompt += f"- Combined market share: {bidder_market_share + target_market_share:.2%}\n"
        prompt += f"- Product overlap: {product_overlap}\n"
        prompt += "- Potential anticompetitive effects (horizontal and/or vertical)\n"
        prompt += "- Impact on market competition and consumer welfare\n\n"
        prompt += "Provide a detailed analysis and assessment of the antitrust risks associated with this merger."

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an antitrust expert providing merger analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=128000,
            n=1,
            stop=None,
            temperature=0.7,
        )

        analysis = response['choices'][0]['message']['content'].strip()
        return f"\n{regulator} Analysis:\n{analysis}\n"

    def identify_regulators(self, bidder_countries, target_countries):
        regulators = []

        if any(country in ["USA", "United States", "US"] for country in bidder_countries + target_countries):
            regulators.extend(["FTC", "DOJ", "FCC", "SEC"])

        if any(country in ["EU", "European Union"] for country in bidder_countries + target_countries):
            regulators.append("DG COMP")

        if "Germany" in bidder_countries + target_countries:
            regulators.append("Bundeskartellamt")

        if "France" in bidder_countries + target_countries:
            regulators.append("Autorité de la Concurrence")

        if "China" in bidder_countries + target_countries:
            regulators.extend(["SAMR", "MOFCOM"])

        return regulators

    def get_approval_timelines(self, regulators):
        timelines = {
            "FTC": 12,
            "DOJ": 12,
            "FCC": 18,
            "SEC": 6,
            "DG COMP": 6,
            "Bundeskartellamt": 4,
            "Autorité de la Concurrence": 6,
            "SAMR": 6,
            "MOFCOM": 6
        }

        return {regulator: timelines[regulator] for regulator in regulators}

    def calculate_approval_probability(self, bidder_market_share, target_market_share, product_overlap):
        combined_market_share = bidder_market_share + target_market_share

        if combined_market_share > 0.5:
            probability = 0.2
        elif combined_market_share > 0.4:
            probability = 0.4
        elif combined_market_share > 0.3:
            probability = 0.6
        else:
            probability = 0.8

        if product_overlap == "High Overlap":
            probability *= 0.8
        elif product_overlap == "Moderate Overlap":
            probability *= 0.9

        return probability

api_key = "sk-proj-PKgDjGHcIXNFyD81FAvbT3BlbkFJgAznkk29REnk0QTOUqfu"  # Replace with your OpenAI API key

root = ttk.Window(themename="superhero")
merger_analysis_tool = MergerAnalysisTool(root, api_key)
root.mainloop()