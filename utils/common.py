from PIL import Image
import matplotlib.pyplot as plt


def tensor2im(var, normalize=True):
	var = var.cpu().detach().transpose(0, 2).transpose(0, 1).numpy()
	if normalize:
		var = ((var + 1) / 2)
		var[var < 0] = 0
		var[var > 1] = 1
	var = var * 255

	if var.shape[-1] == 1:
		var = var[..., 0]

	return Image.fromarray(var.astype('uint8'))


def vis_images(log_hooks):
	display_count = len(log_hooks)
	fig = plt.figure(figsize=(8, 4 * display_count))
	gs = fig.add_gridspec(display_count, 3)
	for i in range(display_count):
		hooks_dict = log_hooks[i]
		fig.add_subplot(gs[i, 0])
		if 'diff_input' in hooks_dict:
			vis_images_with_id(hooks_dict, fig, gs, i)
		else:
			vis_images_no_id(hooks_dict, fig, gs, i)
	plt.tight_layout()
	return fig


def vis_images_with_id(hooks_dict, fig, gs, i):
	plt.imshow(hooks_dict['input_image'])
	plt.title('Input\nOut Sim={:.2f}'.format(float(hooks_dict['diff_input'])))
	fig.add_subplot(gs[i, 1])
	plt.imshow(hooks_dict['target_image'])
	plt.title('Target\nIn={:.2f}, Out={:.2f}'.format(float(hooks_dict['diff_views']),
													 float(hooks_dict['diff_target'])))
	fig.add_subplot(gs[i, 2])
	plt.imshow(hooks_dict['output_image'])
	plt.title('Output\n Target Sim={:.2f}'.format(float(hooks_dict['diff_target'])))


def vis_images_no_id(hooks_dict, fig, gs, i):
	plt.imshow(hooks_dict['input_image'], cmap="gray")
	plt.title('Input')
	fig.add_subplot(gs[i, 1])
	plt.imshow(hooks_dict['target_image'], cmap="gray")
	plt.title('Target')
	fig.add_subplot(gs[i, 2])
	plt.imshow(hooks_dict['output_image'], cmap="gray")
	plt.title('Output')
