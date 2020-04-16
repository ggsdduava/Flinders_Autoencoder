from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import torch
import numpy
import os
import torchvision
from sklearn.metrics import roc_curve, auc


def poly_lr_scheduler(my_optimizer, init_lr, epoch,
                      lr_decay_iter=1,
                      max_iter=100,
                      power=0.9):
    """Polynomial decay of learning rate
        :param init_lr is base learning rate
        :param epoch is a current epoch
        :param lr_decay_iter how frequently decay occurs, default is 1
        :param max_iter is number of maximum iterations
        :param power is a polymomial power
        :param my_optimizer is optimizer

    """
    if epoch % lr_decay_iter or epoch > max_iter:
        return my_optimizer

    lr = init_lr * (1 - epoch / max_iter) ** power
    for param_group in my_optimizer.param_groups:
        param_group['lr'] = lr
    return lr


def get_current_learning_rate(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']


def mnist_plot_encoded_3d_chart(number_value, encoded_data):
    fig = plt.figure(2)
    ax = Axes3D(fig)
    x_axis, y_axis, z_axis = encoded_data.data[:, 0].cpu().detach().numpy(), \
                             encoded_data.data[:, 1].cpu().detach().numpy(), \
                             encoded_data.data[:, 2].cpu().detach().numpy()

    for x, y, z, s in zip(x_axis, y_axis, z_axis, number_value):
        c = cm.rainbow(int(255 * s / 9))
        ax.text(x, y, z, s, backgroundcolor=c)
    ax.set_xlim(x_axis.min(), x_axis.max())
    ax.set_ylim(y_axis.min(), y_axis.max())
    ax.set_zlim(z_axis.min(), z_axis.max())
    plt.show()


def mnist_get_data_set(dir_path, get_number=None, not_number=None, train=True):
    img_transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize((31, 31)),
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    data_set = torchvision.datasets.MNIST(dir_path, train=train, transform=img_transform)
    idx = 0
    if get_number is not None or not_number is not None:
        if get_number is not None:
            idx = data_set.train_labels == get_number
        elif not_number is not None:
            idx = data_set.train_labels != not_number
        data_set.train_labels = data_set.train_labels[idx]
        data_set.train_data = data_set.train_data[idx]
    return data_set


def plot_2d_chart(x1, y1, label1='predict_results',
                  x2=None, y2=None, label2=None, save_path=None, title=None):
    plt.plot(x1, y1, color='red', label=label1, marker='o', mec='r', mfc='w')
    if x2 is not None and y2 is not None:
        plt.plot(x2, y2, color='green', label=label2, marker='*', mec='g', mfc='w')
        # plt.plot(x2, y2, color='green', label=label2,
        #          marker='o',
        #          mec='green',
        #          mfc='w')
    plt.xlabel('labels')
    plt.xticks(rotation=45)
    plt.ylabel('loss')
    plt.legend()
    if title is not None:
        plt.title(title)
    else:
        plt.title('line_chart_for_anomaly_detector')
    plt.grid()
    if save_path is not None:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()


def view_images(title_list, image_list, task_title=None, size=5, axis=False):
    row = numpy.int(numpy.ceil(len(image_list) / 2))
    column = numpy.int(numpy.ceil(len(image_list) / row))
    plt.figure(task_title)
    plt.figure(task_title, figsize=(size, size))
    for col_index in range(column):
        for row_index in range(row):
            num = col_index * row + row_index
            if num == len(image_list) or num == len(title_list):
                break
            plt.subplot(row, column, num + 1)
            plt.title(title_list[num])
            if not axis:
                plt.axis('off')
            plt.imshow(image_list[num])

    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()


def plot_abnormal_normal_chart(abnormal, normal,
                               save=None, show=False):
    plt.plot(numpy.arange(0, 128), abnormal, color='red', label='abnormal_only_zeros ',
             marker='o',
             mec='r', mfc='w')

    plt.plot(numpy.arange(128, 256), normal, color='green', label='normal_no_zeros',
             marker='o',
             mec='green',
             mfc='w')
    plt.xlabel('labels')
    plt.xticks(rotation=45)
    plt.ylabel('loss')
    plt.legend()
    plt.title('line_chart_for_anomaly_detector')
    plt.grid()
    if show:
        plt.show()
    if save is not None:
        dir_path = str(save).split('/')[0]
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        plt.savefig('{}.png'.format(save))
    plt.close()


def mnist_get_visualize_data(input_image, output_image):
    pic_total_1 = numpy.array(input_image[0])
    for i in range(input_image.shape[0] - 1):
        pic_total_1 = numpy.concatenate((pic_total_1, input_image[i + 1]), axis=1)

    pic_total_2 = numpy.array(output_image[0])
    for i in range(output_image.shape[0] - 1):
        pic_total_2 = numpy.concatenate((pic_total_2, output_image[i + 1]), axis=1)
    pic_total = numpy.concatenate((pic_total_1, pic_total_2), axis=0)
    return pic_total


def draw_roc(tp_list, fp_list, title=None):
    # auc drawing
    auc_curve = auc(fp_list, tp_list)

    plt.plot(fp_list, tp_list, color='red', label='AUC area:(%0.5f)' % auc_curve)
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.xlim([-0.005, 1.005])
    plt.ylim([-0.005, 1.005])
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    if title is not None:
        plt.title('Roc_Curve based on {}'.format(title))
    plt.legend(loc='lower right')
    plt.grid()
    plt.show()


def tmp():
    tp_list_19 = [0.0, 0.0, 0.0, 0.0, 0.045454545454545456, 0.045454545454545456, 0.09090909090909091, 0.09090909090909091, 0.13636363636363635, 0.18181818181818182, 0.3181818181818182, 0.36363636363636365, 0.36363636363636365, 0.4090909090909091, 0.45454545454545453, 0.5909090909090909, 0.6818181818181818, 0.7272727272727273, 0.7272727272727273, 0.7727272727272727, 0.9090909090909091, 0.9090909090909091, 0.9090909090909091, 0.9090909090909091, 0.9090909090909091, 0.9090909090909091, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 1.0, 1.0, 1.0]

    fp_list_19 =[0.0, 0.014705882352941176, 0.014705882352941176, 0.014705882352941176, 0.029411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.058823529411764705, 0.07352941176470588, 0.08823529411764706, 0.1323529411764706, 0.1323529411764706, 0.14705882352941177, 0.20588235294117646, 0.22058823529411764, 0.23529411764705882, 0.23529411764705882, 0.27941176470588236, 0.3235294117647059, 0.36764705882352944, 0.4411764705882353, 0.5147058823529411, 0.6029411764705882, 0.7205882352941176, 0.7794117647058824, 0.7941176470588235, 0.8088235294117647, 0.8382352941176471, 0.8382352941176471, 0.8676470588235294, 0.8970588235294118, 0.9117647058823529, 0.9117647058823529, 0.9264705882352942, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9705882352941176, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 1.0]

    tp_list_16 =[0.0, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.13636363636363635, 0.13636363636363635, 0.18181818181818182, 0.18181818181818182, 0.3181818181818182, 0.3181818181818182, 0.36363636363636365, 0.4090909090909091, 0.45454545454545453, 0.5, 0.6818181818181818, 0.6818181818181818, 0.7727272727272727, 0.8181818181818182, 0.8636363636363636, 0.8636363636363636, 0.8636363636363636, 0.8636363636363636, 0.8636363636363636, 0.9090909090909091, 0.9090909090909091, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    fp_list_16 =[0.0, 0.0, 0.0, 0.014705882352941176, 0.014705882352941176, 0.014705882352941176, 0.014705882352941176, 0.014705882352941176, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.058823529411764705, 0.07352941176470588, 0.11764705882352941, 0.14705882352941177, 0.17647058823529413, 0.17647058823529413, 0.19117647058823528, 0.23529411764705882, 0.29411764705882354, 0.29411764705882354, 0.3382352941176471, 0.3382352941176471, 0.39705882352941174, 0.39705882352941174, 0.45588235294117646, 0.5147058823529411, 0.5588235294117647, 0.5882352941176471, 0.6323529411764706, 0.6911764705882353, 0.7794117647058824, 0.8235294117647058, 0.8382352941176471, 0.8382352941176471, 0.8823529411764706, 0.9411764705882353, 0.9411764705882353, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 1.0]

    tp_list_13 =[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.045454545454545456, 0.045454545454545456, 0.09090909090909091, 0.18181818181818182, 0.22727272727272727, 0.3181818181818182, 0.3181818181818182, 0.36363636363636365, 0.36363636363636365, 0.4090909090909091, 0.5, 0.5454545454545454, 0.6818181818181818, 0.7727272727272727, 0.7727272727272727, 0.8181818181818182, 0.8181818181818182, 0.8636363636363636, 0.8636363636363636, 0.9090909090909091, 0.9090909090909091, 0.9090909090909091, 0.9090909090909091, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    fp_list_13 =[0.0, 0.014705882352941176, 0.014705882352941176, 0.014705882352941176, 0.014705882352941176, 0.014705882352941176, 0.014705882352941176, 0.014705882352941176, 0.014705882352941176, 0.014705882352941176, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.058823529411764705, 0.08823529411764706, 0.08823529411764706, 0.10294117647058823, 0.10294117647058823, 0.11764705882352941, 0.1323529411764706, 0.16176470588235295, 0.16176470588235295, 0.22058823529411764, 0.22058823529411764, 0.23529411764705882, 0.2647058823529412, 0.29411764705882354, 0.3088235294117647, 0.3235294117647059, 0.3382352941176471, 0.35294117647058826, 0.38235294117647056, 0.4117647058823529, 0.4117647058823529, 0.47058823529411764, 0.5, 0.5147058823529411, 0.5441176470588235, 0.5441176470588235, 0.5588235294117647, 0.5588235294117647, 0.6470588235294118, 0.7205882352941176, 0.7352941176470589, 0.7647058823529411, 0.8088235294117647, 0.8235294117647058, 0.8676470588235294, 0.8823529411764706, 0.8823529411764706, 0.9117647058823529, 0.9264705882352942, 0.9264705882352942, 0.9264705882352942, 0.9411764705882353, 0.9411764705882353, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9558823529411765, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 1.0]

    tp_list_11 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.045454545454545456, 0.13636363636363635, 0.13636363636363635, 0.18181818181818182, 0.18181818181818182, 0.2727272727272727, 0.2727272727272727, 0.3181818181818182, 0.3181818181818182, 0.36363636363636365, 0.4090909090909091, 0.45454545454545453, 0.5, 0.5454545454545454, 0.5454545454545454, 0.5909090909090909, 0.6818181818181818, 0.7272727272727273, 0.7727272727272727, 0.8181818181818182, 0.8181818181818182, 0.8181818181818182, 0.8636363636363636, 0.9090909090909091, 0.9090909090909091, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 0.9545454545454546, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    fp_list_11 = [0.0, 0.014705882352941176, 0.014705882352941176, 0.014705882352941176, 0.029411764705882353, 0.029411764705882353, 0.029411764705882353, 0.029411764705882353, 0.029411764705882353, 0.029411764705882353, 0.029411764705882353, 0.029411764705882353, 0.029411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.04411764705882353, 0.058823529411764705, 0.08823529411764706, 0.08823529411764706, 0.10294117647058823, 0.10294117647058823, 0.11764705882352941, 0.1323529411764706, 0.14705882352941177, 0.17647058823529413, 0.20588235294117646, 0.25, 0.25, 0.27941176470588236, 0.29411764705882354, 0.29411764705882354, 0.3382352941176471, 0.38235294117647056, 0.4117647058823529, 0.4264705882352941, 0.4264705882352941, 0.4411764705882353, 0.47058823529411764, 0.5, 0.5294117647058824, 0.5441176470588235, 0.5588235294117647, 0.5735294117647058, 0.5735294117647058, 0.5735294117647058, 0.6029411764705882, 0.6176470588235294, 0.6617647058823529, 0.7352941176470589, 0.7647058823529411, 0.7794117647058824, 0.8382352941176471, 0.8529411764705882, 0.8970588235294118, 0.9117647058823529, 0.9411764705882353, 0.9411764705882353, 0.9411764705882353, 0.9411764705882353, 0.9558823529411765, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9705882352941176, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 0.9852941176470589, 1.0]

    tp_list_8 =[0.0004173946799710393, 0.00041607252205722034, 0.0003797523386310786, 0.0005481570842675865, 0.0006221806979738176, 0.0005987709737382829, 0.000603271066211164, 0.0004287679330445826, 0.0011843758402392268, 0.00047399685718119144, 0.0004161511023994535, 0.0005878405645489693, 0.00043486084905453026, 0.0005654919077642262, 0.0005757958861067891, 0.0007132759201340377, 0.0005404084804467857, 0.0004380255122669041, 0.0005104775191284716, 0.0006174270529299974, 0.00037173100281506777, 0.0004246117314323783]
    fp_list_8 =[0.0007787602371536195, 0.0009948278311640024, 0.0009300585370510817, 0.0011915991781279445, 0.0007856899756006896, 0.0010759880533441901, 0.0010735257528722286, 0.00030723793315701187, 0.0009041508892551064, 0.0008234860142692924, 0.0008725247462280095, 0.0011509512551128864, 0.000978205120190978, 0.0008072915952652693, 0.0008880282402969897, 0.0010094518074765801, 0.0007115572225302458, 0.0009702036622911692, 0.000867950904648751, 0.0008065608562901616, 0.000869302311912179, 0.0009345827857032418, 0.001685144379734993, 0.0006622225046157837, 0.0003642069350462407, 0.0010993070900440216, 0.0011099292896687984, 0.0008727003005333245, 0.0007216688827611506, 0.0009549309615977108, 0.0010405394714325666, 0.0009145298972725868, 0.001055789995007217, 0.0016175324562937021, 0.0007070186547935009, 0.0009187828982248902, 0.0007321329903788865, 0.0009568817913532257, 0.0009282613755203784, 0.0008861006936058402, 0.00101487769279629, 0.0010127436835318804, 0.0009314335766248405, 0.00077119714114815, 0.0007040452910587192, 0.0009308719891123474, 0.0008693363633938134, 0.0009489420335739851, 0.0010027673561125994, 0.000399439042666927, 0.000857646344229579, 0.001037683803588152, 0.0011898924130946398, 0.0008949992479756474, 0.0007312432862818241, 0.0007005567313171923, 0.0007738018757663667, 0.001090262201614678, 0.0007456413004547358, 0.0009389206534251571, 0.0005936725065112114, 0.0006318757077679038, 0.0005026303697377443, 0.0007156834471970797, 0.0010828818194568157, 0.0008421813254244626, 0.000608826638199389, 0.0006068338989280164]

    auc_curve_19 = auc(fp_list_19, tp_list_19)
    auc_curve_16 = auc(fp_list_16, tp_list_16)
    auc_curve_13 = auc(fp_list_13, tp_list_13)
    auc_curve_11 = auc(fp_list_11, tp_list_11)
    auc_curve_8 = auc(fp_list_8, tp_list_8)

    plt.plot(fp_list_19, tp_list_19, color='black', label='VGG 19 AUC area:(%0.5f)' % auc_curve_19)
    plt.plot(fp_list_16, tp_list_16, color='blue', label='VGG 16 AUC area:(%0.5f)' % auc_curve_16)
    plt.plot(fp_list_13, tp_list_13, color='orange', label='VGG 13 AUC area:(%0.5f)' % auc_curve_13)
    plt.plot(fp_list_11, tp_list_11, color='green', label='VGG 11 AUC area:(%0.5f)' % auc_curve_11)
    plt.plot(fp_list_8, tp_list_8, color='red', label='VGG 8 AUC area:(%0.5f)' % auc_curve_8)
    plt.plot([0, 1], [0, 1], linestyle='--')
    plt.xlim([-0.005, 1.005])
    plt.ylim([-0.005, 1.005])
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.title('')
    plt.legend(loc='lower right')
    plt.grid()
    plt.show()
