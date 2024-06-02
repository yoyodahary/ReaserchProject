if not os.path.exists(results_path):
    os.makedirs(results_path)
for preprocessing in preprocessings:
  folder = results_path + preprocessing
  if not os.path.exists(folder):
    os.makedirs(folder)
  for amount in NUMBER_OF_WORDS:
    amount_folder = folder + '/' + str(amount)
    if not os.path.exists(amount_folder):
      os.makedirs(amount_folder)
    for column in COLUMNS:
      column_folder = amount_folder + '/' + column
      if not os.path.exists(column_folder):
        os.makedirs(column_folder)
      for oversampler in OVERSAMPLERS:
        oversampler_folder = column_folder + '/' + oversampler
        if not os.path.exists(oversampler_folder):
          os.makedirs(oversampler_folder)
