import torch
import torch.nn as nn
import torch.nn.functional as F
# import cpp_master_bridge as c_net 

class DistributedMulticlassClassifier(nn.Module):
    def __init__(self, input_dim: int, num_classes: int, hidden1: int = 128, hidden2: int = 64):
        super(DistributedMulticlassClassifier, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden1)
        self.fc2 = nn.Linear(hidden1, hidden2)
        self.class_logits = nn.Linear(hidden2, num_classes)
        self.class_log_vars = nn.Linear(hidden2, num_classes)

    def forward(self, x: torch.Tensor):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        
        # convertimos el tensor a NumPy (puntero de memoria) y lo enviamos al Distribuidor C++
        # x_np = x.detach().numpy()
        # weights_np = self.class_logits.weight.detach().numpy()
        # distributed_logits = c_net.distribute_matrix_multiplication(x_np, weights_np)
        # logits = torch.tensor(distributed_logits)
        
        logits = self.class_logits(x) # Backup nativo temporal
        log_vars = self.class_log_vars(x)
        return logits, log_vars
