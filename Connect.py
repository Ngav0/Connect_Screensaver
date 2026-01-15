import tkinter as tk
import random
import math

class ChillGlowScreensaver:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none")  # Hide cursor
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.canvas = tk.Canvas(root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.num_points = 80
        self.max_distance = 150
        self.points = []

        # Initialize random points
        for _ in range(self.num_points):
            point = {
                "x": random.uniform(0, self.width),
                "y": random.uniform(0, self.height),
                "vx": random.uniform(-0.8, 0.8),
                "vy": random.uniform(-0.8, 0.8),
                "size": random.uniform(2, 5),
                "base_brightness": random.uniform(0.4, 0.8),
                "pulse_speed": random.uniform(0.01, 0.04),
                "pulse_phase": random.uniform(0, 2 * math.pi),
                "brightness": 0,
            }
            self.points.append(point)

        self.time = 0
        self.animate()

    def clamp(self, val, min_val=0, max_val=255):
        return max(min_val, min(max_val, int(val)))

    def animate(self):
        self.canvas.delete("all")

        for p in self.points:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["x"] < 0 or p["x"] > self.width:
                p["vx"] *= -1
            if p["y"] < 0 or p["y"] > self.height:
                p["vy"] *= -1

            raw_brightness = p["base_brightness"] + 0.4 * math.sin(self.time * p["pulse_speed"] + p["pulse_phase"])
            p["brightness"] = max(0, min(1, raw_brightness))

        # Draw connections between points
        for i, p1 in enumerate(self.points):
            for j in range(i + 1, len(self.points)):
                p2 = self.points[j]
                dist = math.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"])
                if dist < self.max_distance:
                    avg_brightness = (p1["brightness"] + p2["brightness"]) / 2
                    line_alpha = (1 - dist / self.max_distance) * avg_brightness * 255
                    a = self.clamp(line_alpha)
                    color = f"#{a:02x}{a:02x}{a:02x}"
                    self.canvas.create_line(p1["x"], p1["y"], p2["x"], p2["y"], fill=color, width=1)

        # Draw the points
        for p in self.points:
            alpha = self.clamp(p["brightness"] * 255)
            color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
            r = p["size"]
            self.canvas.create_oval(p["x"] - r, p["y"] - r, p["x"] + r, p["y"] + r, fill=color, outline="")

        self.time += 1
        self.root.after(30, self.animate)

def main():
    root = tk.Tk()
    ChillGlowScreensaver(root)
    root.mainloop()

if __name__ == "__main__":
    main()