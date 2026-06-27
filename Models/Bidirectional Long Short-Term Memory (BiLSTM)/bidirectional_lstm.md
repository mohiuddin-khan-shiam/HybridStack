# Bidirectional Long Short-Term Memory (BiLSTM)

## 1. Background and Context
The **Bidirectional Long Short-Term Memory (BiLSTM)** network is an advanced recurrent neural network (RNN) architecture introduced by Alex Graves and Jürgen Schmidhuber in 2005, building upon the standard LSTM design formulated by Sepp Hochreiter and Jürgen Schmidhuber in 1997. 

Traditional unidirectional LSTMs process sequential input data exclusively in chronological order (forward in time). This unidirectional constraint means that at any given step $t$, the hidden state vector contains information gathered solely from historical context ($t-1, t-2, \dots$). However, in many sequential domains—such as natural language processing, audio interpretation, and non-causal time-series analysis—understanding the structural dependencies of a given step requires looking simultaneously at historical context and future developments. BiLSTMs address this by processing data in both directions through two separate recurrent streams, combining past and future contextual windows to construct a richer sequence representation.

---

## 2. Theoretical Framework and Mathematical Equations

### 2.1. The LSTM Core Cell Architecture
A standard LSTM layer controls information flow via an internal memory cell $c_t$ governed by three differentiable gating mechanisms: the **forget gate** ($f_t$), the **input gate** ($i_t$), and the **output gate** ($o_t$). Given an input vector $\mathbf{x}_t$ and a previous hidden state $\mathbf{h}_{t-1}$, the cell transitions are calculated as follows:

1. **Forget Gate:** Decides what information to discard from the previous cell state.
   $$f_t = \sigma\left(\mathbf{W}_f \mathbf{x}_t + \mathbf{U}_f \mathbf{h}_{t-1} + \mathbf{b}_f\right)$$
2. **Input Gate & Candidate Cell State:** Controls what new information to write into the cell state.
   $$i_t = \sigma\left(\mathbf{W}_i \mathbf{x}_t + \mathbf{U}_i \mathbf{h}_{t-1} + \mathbf{b}_i\right)$$
   $$\tilde{c}_t = \tanh\left(\mathbf{W}_c \mathbf{x}_t + \mathbf{U}_c \mathbf{h}_{t-1} + \mathbf{b}_c\right)$$
3. **Cell State Update:** Combines the historical cell state and the new candidate state.
   $$c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$$
4. **Output Gate & Hidden State:** Computes the updated hidden state to pass to the next time step.
   $$o_t = \sigma\left(\mathbf{W}_o \mathbf{x}_t + \mathbf{U}_o \mathbf{h}_{t-1} + \mathbf{b}_o\right)$$
   $$\mathbf{h}_t = o_t \odot \tanh(c_t)$$

where $\sigma(z) = \frac{1}{1 + e^-z}$ is the sigmoid activation function, $\odot$ denotes the Hadamard (element-wise) product, and $\mathbf{W}, \mathbf{U}, \mathbf{b}$ represent the weight matrices and bias vectors.

### 2.2. The Bidirectional Paradigm
A BiLSTM duplicates the recurrent structure, feeding the input sequence into a forward LSTM layer and a backward LSTM layer simultaneously. 



Let $\overrightarrow{\mathbf{h}}_t$ be the hidden state of the forward LSTM layer, which processes data from $t=1$ to $t=T$. Let $\overleftarrow{\mathbf{h}}_t$ be the hidden state of the backward LSTM layer, which processes data from $t=T$ to $t=1$:

$$\overrightarrow{\mathbf{h}}_t = \text{LSTM}_{\text{forward}}\left(\mathbf{x}_t, \overrightarrow{\mathbf{h}}_{t-1}\right)$$
$$\overleftarrow{\mathbf{h}}_t = \text{LSTM}_{\text{backward}}\left(\mathbf{x}_t, \overleftarrow{\mathbf{h}}_{t+1}\right)$$

The complete contextual hidden state $\mathbf{y}_t$ at index $t$ is formed by concatenating or summing the outputs of the two opposing streams:

$$\mathbf{y}_t = \left[ \overrightarrow{\mathbf{h}}_t \, \Vert \, \overleftarrow{\mathbf{h}}_t \right]$$

where $\Vert$ represents the vector concatenation operator. If each directional layer contains $M$ hidden units, the resulting vector dimensions expand to $2M$.

---

## 3. Algorithm Description

1. **Input Reshaping:** Convert the input array from a 2D form (samples, features) into a 3D tensor format required by recurrent networks: `(samples, timesteps, features)`.
2. **Forward and Backward Inference Passes:**
    * The forward stream processes the input tensor chronologically, computing and storing hidden states $\overrightarrow{\mathbf{h}}_t$.
    * The backward stream processes the input tensor in reverse chronological order, computing and storing hidden states $\overleftarrow{\mathbf{h}}_t$.
3. **Hidden State Fusion:** Concatenate the corresponding hidden states at each time step to construct a combined bidirectional hidden representation.
4. **Stacked Recurrent Processing:** Pass the sequence of concatenated vectors through a second BiLSTM layer to extract higher-level temporal patterns.
5. **Regression Projection:** Pass the final time step's hidden state through a fully connected linear layer (`Dense(1)`) to map the hidden features to a single continuous target prediction.