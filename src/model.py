import torch
import torch.nn as nn


class ECG_CNN(nn.Module):

    def __init__(self):
        super().__init__()

        self.features = nn.Sequential(

            nn.Conv1d(
                1,
                12,
                kernel_size=5,
                padding=2
            ),

            nn.ReLU(),

            nn.Conv1d(
                12,
                24,
                kernel_size=5,
                padding=2
            ),

            nn.ReLU(),

            nn.AdaptiveAvgPool1d(1)

        )

        self.classifier = nn.Linear(24,2)

    def forward(self,x):

        x=self.features(x)

        x=x.squeeze(-1)

        x=self.classifier(x)

        return x


if __name__=="__main__":

    model=ECG_CNN()

    x=torch.randn(2,1,256)

    y=model(x)

    print(model)

    print(y.shape)