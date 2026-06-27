# Bidirectional Gated Recurrent Unit (BiGRU)

## 1. Background and Context
The **Bidirectional Gated Recurrent Unit (BiGRU)** is an advanced recurrent neural network (RNN) architecture designed for processing sequential data. It combines the gated recurrent mechanisms introduced by Cho et al. in 2014 with the bidirectional processing paradigm pioneered by Schuster and Paliwal in 1997.

Standard unidirectional RNNs suffer from vanishing and exploding gradient problems when learning long-term dependencies. While the Long Short-Term Memory (LSTM) network addresses this by using a complex three-gate architecture, the Gated Recurrent Unit (GRU) offers a streamlined alternative. By coupling the forget and input gates into a single update gate and merging the cell state and hidden state, the GRU reduces computational complexity and parameter counts while maintaining competitive performance.

Unidirectional models only process information chronologically, meaning that the hidden state at time $t$ relies entirely on past inputs ($t-1, t-2, \dots$). However, many sequential problems exhibit context dependencies spanning both directions. A BiGRU duplicates the hidden layer to process inputs in both forward and backward directions simultaneously, capturing past and future context at every sequence step.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. The GRU Cell Mechanics
A GRU cell regulates information flow inside its recurrent state without an independent memory cell container. It achieves this using two functional gating networks: the **update gate** ($z_t$) and the **reset gate** ($r_t$). Given an input vector $\mathbf{x}_t$ and the preceding hidden state vector $\mathbf{h}_{t-1}$, the cell state updates sequentially:

1. **Update Gate:** Dictates the proportion of historical information to retain alongside new candidate state metrics.
   $$z_t = \sigma\left(\mathbf{W}_z \mathbf{x}_t + \mathbf{U}_z \mathbf{h}_{t-1} + \mathbf{b}_z\right)$$
2. **Reset Gate:** Determines how much of the past hidden state to forget when computing the new candidate state.
   $$r_t = \sigma\left(\mathbf{W}_r \mathbf{x}_t + \mathbf{U}_r \mathbf{h}_{t-1} + \mathbf{b}_r\right)$$
3. **Candidate Hidden State:** Constructs a new hidden state candidate using the reset gate to scale historical contributions.
   $$\tilde{\mathbf{h}}_t = \tanh\left(\mathbf{W}_h \mathbf{x}_t + \mathbf{U}_h \left(\mathbf{r}_t \odot \mathbf{h}_{t-1}\right) + \mathbf{b}_h\right)$$
4. **Final Hidden State:** Linearly interpolates between the previous hidden state and the new candidate state using the update gate.
   $$\mathbf{h}_t = \left(1 - z_t\right) \odot \mathbf{h}_{t-1} + z_t \odot \tilde{\mathbf{h}}_t$$

where $\sigma(z) = \frac{1}{1 + e^{-z}}$ is the sigmoid activation function, $\odot$ denotes the Hadamard (element-wise) matrix product, and $\mathbf{W}$, $\mathbf{U}$, and $\mathbf{b}$ represent the learned weight matrices and bias vectors, respectively.

### 2.2. The Bidirectional Structure
A BiGRU processes the input sequence using two independent GRU streams in opposite directions. 



Let $\overrightarrow{\mathbf{h}}_t$ be the hidden state of the forward GRU layer, which processes information from step $t=1$ to $t=T$. Let $\overleftarrow{\mathbf{h}}_t$ be the hidden state of the backward GRU layer, which processes information from step $t=T$ to $t=1$:

$$\overrightarrow{\mathbf{h}}_t = \text{GRU}_{\text{forward}}\left(\mathbf{x}_t, \overrightarrow{\mathbf{h}}_{t-1}\right)$$
$$\overleftarrow{\mathbf{h}}_t = \text{GRU}_{\text{backward}}\left(\mathbf{x}_t, \overleftarrow{\mathbf{h}}_{t+1}\right)$$

The final comprehensive representation at step $t$ is constructed by concatenating the hidden state vectors from both streams:

$$\mathbf{y}_t = \left[ \overrightarrow{\mathbf{h}}_t \, \Vert \, \overleftarrow{\mathbf{h}}_t \right]$$

where $\Vert$ represents the vector concatenation operator. If each direction contains $M$ units, the resulting dimensionality expands to $2M$, encoding bidirectional context simultaneously.

---

## 3. Algorithm Description

1. **Sequential Tensor Structuring:** Reshape the input feature matrices into a 3D tensor format mapping `(samples, timesteps, features)` to satisfy recurrent layer requirements.
2. **Dual-Stream Processing Block:**
    * The forward GRU layer evaluates input windows sequentially, outputting chronological hidden streams $\overrightarrow{\mathbf{h}}_t$.
    * The backward GRU layer evaluates input windows in reverse chronological order, outputting reverse hidden streams $\overleftarrow{\mathbf{h}}_t$.
3. **Context Feature Fusion:** Concatenate the corresponding forward and backward hidden state vectors at each time step.
4. **Stacked Recurrent Routing:** Feed the sequences from the initial bidirectional block into a second tracking BiGRU layer to extract deeper temporal abstractions.
5. **Linear Target Projection:** Map the final hidden state through a fully connected dense layer (`Dense(1)`) to output a continuous target regression value.