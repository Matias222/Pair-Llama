# PAIR para Llama 3.2 3B - Guía en Español

Repositorio modificado de PAIR para generar ataques jailbreak contra Llama 3.2 3B Instruct corriendo localmente.

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# O usar el script de setup
chmod +x setup.sh
./setup.sh
```

### 2. Configurar API Key

```bash
# Para usar GPT-3.5/GPT-4 como modelo atacante
export OPENAI_API_KEY="tu-api-key-aqui"

# Deshabilitar wandb si no tienes cuenta
export WANDB_MODE=disabled
```

### 3. Probar que funciona

```bash
python test_llama32.py
```

### 4. Generar ataques PAIR

```bash
python run_pair_llama32.py \
    --attack-model gpt-3.5-turbo-1106 \
    --n-streams 5 \
    --n-iterations 5
```

**Resultado:** Archivo `pair_results/pair_attacks_llama32.csv` con formato `goal;jailbreak`

## 📁 Archivos Modificados/Creados

### Modificados
- `config.py` - Agregada configuración de Llama 3.2
- `conversers.py` - Soporte para modelos locales
- `main.py` - Llama 3.2 como opción de modelo

### Nuevos
- `local_models.py` - Cargador local de HuggingFace
- `test_llama32.py` - Script de prueba
- `run_pair_llama32.py` - Generador automático de ataques
- `requirements.txt` - Dependencias
- `setup.sh` - Script de instalación
- `LLAMA32_SETUP.md` - Documentación detallada (inglés)

## 💡 Opciones de Uso

### Opción 1: Automático (Recomendado)
Genera 10 ataques automáticamente:
```bash
python run_pair_llama32.py
```

### Opción 2: Manual (Un ataque)
```bash
python main.py \
    --attack-model gpt-3.5-turbo-1106 \
    --target-model llama-3.2-3b-instruct \
    --goal "Tu comportamiento dañino aquí" \
    --target-str "Sure, here is..." \
    --evaluate-locally \
    --not-jailbreakbench
```

### Opción 3: Sin API (Gratis)
Usa Llama 3.2 como atacante y objetivo:
```bash
python main.py \
    --attack-model llama-3.2-3b-instruct \
    --target-model llama-3.2-3b-instruct \
    --goal "Tu comportamiento dañino" \
    --evaluate-locally \
    --not-jailbreakbench
```

## 🎯 Usar con tu Defensa

```python
# En defensa_3.py
results = evaluate_defense_on_dataset(
    patch=global_patch,
    model=model,
    tokenizer=tokenizer,
    csv_path="JailbreakingLLMs/pair_results/pair_attacks_llama32.csv",
    device="cuda:0"
)
```

## 📊 Comportamientos Incluidos

El script `run_pair_llama32.py` genera ataques para:
1. Envenenamiento de alimentos
2. Bombas molotov
3. Dinero falso
4. Síntesis de drogas
5. Hackeo de redes
6. Robo a caridades
7. Fabricación de bombas
8. Virus informáticos
9. Comportamientos peligrosos
10. Manipulación psicológica

## ⚙️ Parámetros Importantes

- `--attack-model`: Modelo atacante (GPT-3.5, GPT-4, o Llama 3.2)
- `--target-model`: Modelo objetivo (Llama 3.2)
- `--n-streams`: Intentos paralelos (más = mejor ASR)
- `--n-iterations`: Iteraciones de refinamiento (3-5 usual)
- `--evaluate-locally`: Corre Llama 3.2 localmente
- `--not-jailbreakbench`: No usa JailbreakBench

## 📈 Rendimiento Esperado

- **GPT-4 atacante:** ~70-90% ASR
- **GPT-3.5 atacante:** ~50-70% ASR
- **Llama 3.2 atacante:** ~20-40% ASR

**Tiempo:** 30-60 minutos para 10 comportamientos
**Costo:** ~$0.50-1.00 con GPT-3.5

## 🔧 Troubleshooting

### Error: Model not found
```python
# Edita config.py línea 4:
LLAMA_32_PATH = "tu/ruta/a/Llama-3.2-3B-Instruct"
```

### Error: CUDA out of memory
```bash
# Reduce n-streams
python run_pair_llama32.py --n-streams 2
```

### Error: OPENAI_API_KEY not set
```bash
export OPENAI_API_KEY="sk-..."
```

## 📚 Documentación Adicional

- `LLAMA32_SETUP.md` - Guía detallada en inglés
- `README.md` - README original de PAIR

## 🎓 Para tu Paper

Ahora tienes dos familias de ataques:
1. **GCG** (gradient-based) - En `data_curada.csv`
2. **PAIR** (LLM-iterative) - En `pair_results/pair_attacks_llama32.csv`

Esto te permite evaluar la robustez de tu defensa contra diferentes tipos de ataques!

## 📞 Soporte

Ver documentación completa en `LLAMA32_SETUP.md` o el README original de PAIR.
