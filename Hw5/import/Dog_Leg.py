import cv2
import numpy as np

class Dog_Leg(object):

    def __init__(self, inliers1, inliers2, matrix_H):
        self.apply_dog_leg(inliers1, inliers2, matrix_H)

    def get_matrix_H(self):
        return matrix_H

    def find_Jacobian(self, Inliers1, Inliers2, H_matrix):
        inliers_num = Inliers1.shape[1]
        X1_matrix = np.zeros((3, inliers_num))
        X2_matrix = np.zeros((3, inliers_num))
        X2_vector = np.zeros(inliers_num*2)
        f_vector = np.zeros(inliers_num*2)
        Jacobian_f = np.zeros((inliers_num*2, 9))
        Error_vector = np.zeros(inliers_num*2)
        for i in range(inliers_num):
            X1_matrix[0][i] = Inliers1[0][i]
            X1_matrix[1][i] = Inliers1[1][i]
            X1_matrix[2][i] = 1
        
        X2_matrix = np.dot(H_matrix, X1_matrix)
        for i in range(inliers_num):
            X2_vector[2*i] = Inliers2[0][i]
            X2_vector[2*i+1] = Inliers2[1][i]
            f_vector[2*i] = X2_matrix[0][i]/X2_matrix[2][i]
            f_vector[2*i+1] = X2_matrix[1][i]/X2_matrix[2][i]
    
        for i in range(inliers_num):
            Error_vector[2*i] = X2_vector[2*i] - f_vector[2*i]
            Error_vector[2*i+1] = X2_vector[2*i+1] - f_vector[2*i+1]
        
            Jacobian_f[2*i][0] = X1_matrix[0][i] / X2_matrix[2][i]
            Jacobian_f[2*i][1] = X1_matrix[1][i] / X2_matrix[2][i]
            Jacobian_f[2*i][2] = 1 / X2_matrix[2][i]
            Jacobian_f[2*i][6] = -X2_matrix[0][i] * X1_matrix[0][i] / np.power(X2_matrix[2][i],2)
            Jacobian_f[2*i][7] = -X2_matrix[0][i] * X1_matrix[1][i] / np.power(X2_matrix[2][i],2)
            Jacobian_f[2*i][8] = -X2_matrix[0][i] / np.power(X2_matrix[2][i],2)
        
            Jacobian_f[2*i+1][3] = X1_matrix[0][i] / X2_matrix[2][i]
            Jacobian_f[2*i+1][4] = X1_matrix[1][i] / X2_matrix[2][i]
            Jacobian_f[2*i+1][5] = 1 / X2_matrix[2][i]
            Jacobian_f[2*i+1][6] = -X2_matrix[1][i] * X1_matrix[0][i] / np.power(X2_matrix[2][i],2)
            Jacobian_f[2*i+1][7] = -X2_matrix[1][i] * X1_matrix[1][i] / np.power(X2_matrix[2][i],2)
            Jacobian_f[2*i+1][8] = -X2_matrix[1][i] / np.power(X2_matrix[2][i],2)
        Error_vector = np.reshape(Error_vector, (inliers_num*2,1))
        return Jacobian_f, Error_vector


    def apply_dog_leg(self, Inliers1, Inliers2, H_matrix):
        tau = 0.1
        radius = 10
        n_iterations = 50
        inliers_num = Inliers1.shape[1]
        I_matrix = np.identity(9)
    
        Jacobian_f, Error_vector = self.find_Jacobian(Inliers1, Inliers2, H_matrix)
        Diag = np.dot(Jacobian_f.T, Jacobian_f)
    
        u = Diag[0][0]
        for i in range(9):
            if(Diag[i][i] > u):
                u = Diag[i][i]
            
        u = tau * u
    
        p0 = np.reshape(H_matrix, (9,1))
        Cp0 = np.power(np.linalg.norm(Error_vector), 2)
    
        for i in range(n_iterations):
      
            Jacobian_f0, Error_vector0 = self.find_Jacobian(Inliers1, Inliers2, H_matrix)    
            delta_GD_numerator0 = np.linalg.norm(np.dot(Jacobian_f0.T, Error_vector0))
            delta_GD_denom0 = np.linalg.norm(np.dot(np.dot(Jacobian_f0, Jacobian_f0.T), Error_vector0))
            delta_GD = delta_GD_numerator0 * np.dot(Jacobian_f0.T, Error_vector0)/delta_GD_denom0
        
            delta_GN_numerator = np.dot(Jacobian_f0.T, Error_vector0)
            delta_GN_denom = np.dot(Jacobian_f0.T, Jacobian_f0) + u * I_matrix
            delta_GN = delta_GN_numerator/delta_GN_denom
        
            Cp0 = np.power(np.linalg.norm(Error_vector0), 2)
        
            if(np.linalg.norm(delta_GN) < radius):
                p1 = p0 + delta_GN
            elif(np.linalg.norm(delta_GD) < radius and np.linalg.norm(delta_GN) > radius):
                coeff_a = np.power(np.linalg.norm(delta_GN-delta_GD),2)
                coeff_b = 2 * delta_GD.T * (delta_GN-delta_GD)
                coeff_c = np.power(np.linalg.norm(delta_GD),2) - np.power(radius,2)
                coeff = [coeff_a, coeff_b, coeff_c]
                beta1, beta2 = np.roots(coeff)
                #find the appropriate beta
                if(beta1 >= 0 and beta2 <= 0):
                    beta = beta1
                elif(beta1 <= 0 and beta2 >= 0):
                    beta = beta2
                elif(beta1 >= 0 and beta2 >= 0):
                    if(beta1 < beta2):
                        beta = beta1
                    else:
                        beta = beta2
                else:
                    if(beta1 < beta2):
                        beta = beta2
                    else:
                        beta = beta2
                    
                p1 = p0 + delta_GD + beta*(delta_GN-delta_GD)
            else:
                p1 = p0 + radius*delta_GD/np.linalg.norm(delta_GD)
        
            delta = p1 - p0
            H_matrix1 = np.reshape(p1, (3,3))
        
        
            Jacobian_f1, Error_vector1 = self.find_Jacobian(Inliers1, Inliers2, H_matrix1)
            Cp1 = np.power(np.linalg.norm(Error_vector1), 2)
        
            rho_numerator = Cp0 - Cp1
            rho_denom = 2*np.dot(np.dot(delta.T,Jacobian_f0.T), Error_vector0) - np.dot(np.dot(np.dot(delta.T, Jacobian_f0.T),Jacobian_f0), delta)
            rho = rho_numerator/rho_denom
            if(rho > 0):
                check = 1 - np.power((2*rho-1),3)
                if(check > 1/3): 
                    u = u * check
                else:
                    u = u/3
                H_matrix = H_matrix1
            else:
                u = 2 * u
        
            if(rho > 0 and rho < 0.25):
                radius = radius/4
            elif(rho > 0.25 and rho < 0.75):
                radius = radius
            elif(rho > 0.75):
                radius = 2 * radius
            elif(rho < 0):
                radius = radius/2
    
        self.matrix_H = H_matrix
