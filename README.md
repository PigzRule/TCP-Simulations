# README for TCP Simulations Project

## TCP Simulations: Tahoe, Reno, and Cubic

This project simulates the behavior of **TCP Tahoe**, **TCP Reno**, and **TCP Cubic** using **Python**. Developed for a **Network Security** course, the project provides insights into the congestion control mechanisms of these TCP variants.

---

## Features

- **TCP Tahoe Simulation**  
  Simulates slow start, congestion avoidance, and fast retransmit.

- **TCP Reno Simulation**  
  Adds fast recovery to improve performance during packet loss.

- **TCP Cubic Simulation**  
  Models a high-speed TCP variant optimized for networks with high bandwidth-delay product.

- **Graphical Output**  
  Visualizes the congestion window dynamics over time.

- **Configurable Parameters**  
  Allows users to adjust settings such as packet loss rate and round-trip time.

---

## Technologies Used

- **Python**: Core programming language for simulations.
- **Matplotlib**: For visualizing congestion window changes.
- **NumPy**: To handle data and mathematical computations.

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/PigzRule/TCP-Simulations.git
   ```
2. **Navigate to the Project Directory**  
   ```bash
   cd TCP-Simulations
   ```
3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Run the script to simulate a TCP variant:
   ```bash
   python tcp_simulation.py
   ```
2. Follow the prompts to select a variant (Tahoe, Reno, or Cubic) and configure simulation parameters.

3. View the generated plots to analyze congestion control behavior.

---

## Screenshots

*Coming soon!* Visual representations of TCP simulations.

---

## Contribution

Contributions are welcome!  
1. Fork the repository.  
2. Create a new branch (`git checkout -b feature/your-feature-name`).  
3. Commit your changes (`git commit -m 'Add your message here'`).  
4. Push to the branch (`git push origin feature/your-feature-name`).  
5. Create a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Developed as part of a **Computer Networks** course.
- Inspired by the need to understand TCP congestion control mechanisms in depth.

---

**Explore TCP congestion control with detailed simulations of Tahoe, Reno, and Cubic!**
