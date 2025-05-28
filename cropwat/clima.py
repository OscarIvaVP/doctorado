import pandas as pd

pp = pd.read_excel("precipitacion\pp_subcuencas.xlsx")
tmax = pd.read_excel("clima\\tmax_subcuencas.xlsx")
tmin = pd.read_excel("clima\\tmin_subcuencas.xlsx")

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_temperatures_subplots(df_tmax, df_tmin):
    """
    Genera una cuadrícula de subplots (3 filas, 5 columnas) para mostrar datos de temperatura.
    Cada subplot muestra Tmax y Tmin para una columna de datos común (ej. subcuenca)
    contra la columna 'Fecha'.

    Args:
        df_tmax (pd.DataFrame): DataFrame con datos de Tmax, incluyendo una columna 'Fecha'.
        df_tmin (pd.DataFrame): DataFrame con datos de Tmin, incluyendo una columna 'Fecha'.
    """

    # Función auxiliar para encontrar la columna 'Fecha' (ignora mayúsculas/minúsculas) y procesar el DataFrame
    def process_df(df, df_name_str):
        fecha_col_name = None
        for col in df.columns:
            if col.lower() == 'fecha':
                fecha_col_name = col
                break
        
        if not fecha_col_name:
            print(f"Error: Columna 'Fecha' no encontrada en el DataFrame {df_name_str}.")
            return None, None, None
        
        df_processed = df.copy() # Usar una copia para evitar SettingWithCopyWarning
        try:
            df_processed[fecha_col_name] = pd.to_datetime(df_processed[fecha_col_name])
        except Exception as e:
            print(f"Error al convertir '{fecha_col_name}' a datetime en {df_name_str}: {e}")
            return None, None, None
            
        data_columns = [col for col in df_processed.columns if col != fecha_col_name]
        return df_processed, fecha_col_name, data_columns

    tmax_proc, fecha_col_tmax, tmax_data_cols = process_df(df_tmax, "tmax")
    tmin_proc, fecha_col_tmin, tmin_data_cols = process_df(df_tmin, "tmin")

    if tmax_proc is None or tmin_proc is None:
        print("Generación de gráfico abortada debido a errores en el procesamiento de datos.")
        return

    # Identificar columnas de datos comunes (ej. subcuencas).
    # Se asume que las columnas con el mismo nombre en tmax y tmin se refieren a la misma entidad.
    common_data_cols = sorted(list(set(tmax_data_cols).intersection(set(tmin_data_cols))))

    if not common_data_cols:
        print("No se encontraron columnas de datos comunes (excluyendo 'Fecha') entre los archivos tmax y tmin.")
        print("No se pueden crear gráficos Tmax/Tmin emparejados. Asegúrate de que las columnas de las subcuencas se llamen idénticamente en ambos archivos.")
        return

    num_rows = 3
    num_cols = 5
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(22, 13), sharex=True)
    axes_flat = axes.flatten() # Aplanar para iterar fácilmente

    fig.suptitle('Temperaturas Máximas y Mínimas por Entidad Común', fontsize=16)

    last_plotted_idx = -1
    for idx, data_col_name in enumerate(common_data_cols):
        if idx >= num_rows * num_cols:
            print(f"Advertencia: Mostrando las primeras {num_rows * num_cols} de {len(common_data_cols)} entidades comunes debido al tamaño de la cuadrícula.")
            break

        ax = axes_flat[idx]
        last_plotted_idx = idx
        
        ax.plot(tmax_proc[fecha_col_tmax], tmax_proc[data_col_name], label='Tmax', color='red', linewidth=1.2)
        ax.plot(tmin_proc[fecha_col_tmin], tmin_proc[data_col_name], label='Tmin', color='blue', linewidth=1.2)
        
        ax.set_title(data_col_name, fontsize=11)
        ax.set_ylabel('Temperatura (°C)', fontsize=9) # Asumiendo unidades
        ax.legend(fontsize=8)
        ax.grid(True, linestyle=':', alpha=0.7)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right", fontsize=9)

        current_ax_row = idx // num_cols
        if current_ax_row == num_rows - 1: # Si está en la fila inferior
            ax.set_xlabel('Fecha', fontsize=9)
        else: # No está en la fila inferior
            ax.tick_params(labelbottom=False) # Ocultar etiquetas de ticks del eje X

    # Ocultar subplots no utilizados
    for i in range(last_plotted_idx + 1, len(axes_flat)):
        axes_flat[i].axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajustar rect para suptitle y etiquetas X
    plt.show()

# Ejemplo de cómo llamar a la función con los DataFrames cargados:
plot_temperatures_subplots(tmax, tmin)
