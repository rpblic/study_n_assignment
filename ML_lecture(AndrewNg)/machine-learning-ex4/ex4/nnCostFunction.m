function [J grad] = nnCostFunction(nn_params, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, ...
                                   X, y, lambda)
%NNCOSTFUNCTION Implements the neural network cost function for a two layer
%neural network which performs classification
%   [J grad] = NNCOSTFUNCTON(nn_params, hidden_layer_size, num_labels, ...
%   X, y, lambda) computes the cost and gradient of the neural network. The
%   parameters for the neural network are "unrolled" into the vector
%   nn_params and need to be converted back into the weight matrices. 
% 
%   The returned parameter grad should be a "unrolled" vector of the
%   partial derivatives of the neural network.
%

% Reshape nn_params back into the parameters Theta1 and Theta2, the weight matrices
% for our 2 layer neural network
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1)); %%25*401

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1)); %%10*26

% Setup some useful variables
m = size(X, 1);
         
% You need to return the following variables correctly 
J = 0;
Theta1_grad = zeros(size(Theta1));
Theta2_grad = zeros(size(Theta2));

% ====================== YOUR CODE HERE ======================
% Instructions: You should complete the code by working through the
%               following parts.
%
% Part 1: Feedforward the neural network and return the cost in the
%         variable J. After implementing Part 1, you can verify that your
%         cost function computation is correct by verifying the cost
%         computed in ex4.m
%
% Part 2: Implement the backpropagation algorithm to compute the gradients
%         Theta1_grad and Theta2_grad. You should return the partial derivatives of
%         the cost function with respect to Theta1 and Theta2 in Theta1_grad and
%         Theta2_grad, respectively. After implementing Part 2, you can check
%         that your implementation is correct by running checkNNGradients
%
%         Note: The vector y passed into the function is a vector of labels
%               containing values from 1..K. You need to map this vector into a 
%               binary vector of 1's and 0's to be used with the neural network
%               cost function.
%
%         Hint: We recommend implementing backpropagation using a for-loop
%               over the training examples if you are implementing it for the 
%               first time.
%
% Part 3: Implement regularization with the cost function and gradients.
%
%         Hint: You can implement this around the code for
%               backpropagation. That is, you can compute the gradients for
%               the regularization separately and then add them to Theta1_grad
%               and Theta2_grad from Part 2.
%

X_bias= [ones(m,1) X];
matx_a_2= sigmoid(X_bias*transpose(Theta1)); %%5000*25
a_2_bias= [ones(m,1) matx_a_2]; %%5000*26
matx_a_3= sigmoid(a_2_bias*transpose(Theta2)); %%5000*10
Theta1_nobias= Theta1(:, 2:input_layer_size+1);
Theta2_nobias= Theta2(:, 2:hidden_layer_size+1);

y_vec= zeros(m,num_labels);
for i= 1:m
  y_vec(i, y(i,1))= 1; %% 5000*10
endfor

one_min_y_vec= ones(m, num_labels)- y_vec;

log_a_3= log(matx_a_3);
log_one_min_a_3= log(ones(m, num_labels)-matx_a_3);
J= -(1/m)*(sum(sum((y_vec.*log_a_3.+one_min_y_vec.*log_one_min_a_3), 2))) ...
    + (lambda/(2*m))*(sum(sum(Theta1_nobias.*Theta1_nobias))+sum(sum(Theta2_nobias.*Theta2_nobias)));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
big_lamd1= zeros(hidden_layer_size, input_layer_size+1);
big_lamd2= zeros(num_labels, hidden_layer_size+1);
delta3= transpose(matx_a_3- y_vec); %% 10*5000
delta2= (transpose(Theta2(:,2:hidden_layer_size+1))*delta3).*transpose(matx_a_2).* ...
        transpose(ones(m, hidden_layer_size)-matx_a_2); %% 25*5000

for i= 1:m
  big_lamd2= big_lamd2 .+ delta3(:,i)*a_2_bias(i,:); %% 10*26
endfor

for j= 1:hidden_layer_size+1
  if j==1
    Theta2_grad(:,j)= (1/m)*big_lamd2(:,j);
  else
    Theta2_grad(:,j)= (1/m)*(big_lamd2(:,j)+lambda*Theta2(:,j));
  endif
endfor

for i= 1:m
  big_lamd1= big_lamd1 .+ delta2(:,i)*X_bias(i,:); %% 25*401
endfor

for j= 1:input_layer_size+1
  if j==1
    Theta1_grad(:,j)= (1/m)*big_lamd1(:,j);
  else
    Theta1_grad(:,j)= (1/m)*(big_lamd1(:,j)+lambda*Theta1(:,j));
  endif
endfor











% -------------------------------------------------------------

% =========================================================================

% Unroll gradients
grad = [Theta1_grad(:) ; Theta2_grad(:)];


end
